"""ML Model Service for loading and running PINN models"""
import os
import sys
import yaml
import torch
import numpy as np
from pathlib import Path
from typing import Dict, Optional, Tuple
from flask import current_app

# Add model source code to path
MODEL_BASE_PATH = Path(__file__).parent.parent / 'ml_models' / 'project_1'
sys.path.insert(0, str(MODEL_BASE_PATH))

from src.models.direction_an_pinn import DirectionANPINN
from src.data.preprocess import load_scales, build_context_vector, CONTEXT_FIELDS, Scales


class MLModelService:
    """Service for loading and running ML models"""
    
    _instance = None
    _model = None
    _scales = None
    _config = None
    _context_dim = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLModelService, cls).__new__(cls)
        return cls._instance
    
    def load_model(self, project_id: int = 1) -> bool:
        """
        Load the ML model for a specific project.
        Uses lazy loading - only loads on first request.
        
        Args:
            project_id: Project ID (currently only 1 is supported)
            
        Returns:
            True if model loaded successfully, False otherwise
        """
        if self._model is not None:
            return True
        
        try:
            model_dir = MODEL_BASE_PATH
            checkpoint_path = model_dir / 'best.pt'
            config_path = model_dir / 'config.yaml'
            scales_path = model_dir / 'scales.yaml'
            
            if not checkpoint_path.exists():
                current_app.logger.error(f"Checkpoint not found: {checkpoint_path}")
                return False
            
            if not config_path.exists():
                current_app.logger.error(f"Config not found: {config_path}")
                return False
            
            if not scales_path.exists():
                current_app.logger.error(f"Scales not found: {scales_path}")
                return False
            
            # Load scales
            self._scales = load_scales(str(scales_path))
            
            # Load config
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f)
            
            model_cfg = self._config.get('model', {})
            
            # Determine context dimension (use default 7 for basic fields)
            # In production, this should be loaded from dataset metadata
            self._context_dim = 7  # m0, Isp, Cd, CL_alpha, Cm_alpha, Tmax, wind_mag
            
            # Load physics params (optional - use empty dict if not available)
            physics_params = {}
            physics_config_path = model_dir / 'configs' / 'phys.yaml'
            if physics_config_path.exists():
                with open(physics_config_path, 'r') as f:
                    phys_config = yaml.safe_load(f)
                    if 'aerodynamics' in phys_config:
                        physics_params.update(phys_config['aerodynamics'])
                    if 'propulsion' in phys_config:
                        physics_params.update(phys_config['propulsion'])
                    if 'atmosphere' in phys_config:
                        physics_params.update(phys_config['atmosphere'])
            
            # Convert scales dict to Scales object if needed
            if isinstance(self._scales, dict):
                scales_dict = self._scales.get('scales', self._scales)
                self._scales = Scales(**{k: v for k, v in scales_dict.items() if k in ['L', 'V', 'T', 'M', 'F', 'W']})
            
            # Create model
            model_type = model_cfg.get('type', 'direction_an').lower()
            
            if model_type == 'direction_an':
                self._model = DirectionANPINN(
                    context_dim=self._context_dim,
                    fourier_features=int(model_cfg.get('fourier_features', 8)),
                    stem_hidden_dim=int(model_cfg.get('stem_hidden_dim', 128)),
                    stem_layers=int(model_cfg.get('stem_layers', 4)),
                    activation=model_cfg.get('activation', 'tanh'),
                    layer_norm=bool(model_cfg.get('layer_norm', True)),
                    translation_branch_dims=model_cfg.get('translation_branch_dims', [128, 128]),
                    rotation_branch_dims=model_cfg.get('rotation_branch_dims', [256, 256]),
                    mass_branch_dims=model_cfg.get('mass_branch_dims', [64]),
                    dropout=float(model_cfg.get('dropout', 0.0)),
                    physics_params=physics_params if physics_params else None,
                    physics_scales=self._scales.__dict__ if physics_params else None,
                )
            else:
                current_app.logger.error(f"Unsupported model type: {model_type}")
                return False
            
            # Load checkpoint
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
            
            if 'model_state_dict' in checkpoint:
                self._model.load_state_dict(checkpoint['model_state_dict'])
            else:
                # Try direct state dict
                self._model.load_state_dict(checkpoint)
            
            self._model.eval()
            self._model.to(device)
            
            current_app.logger.info(f"Model loaded successfully for project {project_id}")
            return True
            
        except Exception as e:
            current_app.logger.error(f"Error loading model: {e}", exc_info=True)
            return False
    
    def predict(
        self,
        params: Dict[str, float],
        t_start: float = 0.0,
        t_end: float = 30.0,
        dt: float = 0.02
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict rocket trajectory.
        
        Args:
            params: Dictionary of physical parameters (dimensional units)
            t_start: Start time in seconds
            t_end: End time in seconds
            dt: Time step in seconds
            
        Returns:
            Tuple of (time_array, state_array) where:
            - time_array: [N] time in seconds
            - state_array: [N, 14] state in dimensional units
        """
        if self._model is None or self._scales is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Build context vector
        # Use only fields that are in params
        available_fields = [f for f in CONTEXT_FIELDS if f in params]
        context_normalized = build_context_vector(params, self._scales, fields=available_fields)
        
        # Pad context vector to expected dimension
        if len(context_normalized) < self._context_dim:
            # Pad with zeros
            context_normalized = np.pad(context_normalized, (0, self._context_dim - len(context_normalized)), 'constant')
        elif len(context_normalized) > self._context_dim:
            # Truncate
            context_normalized = context_normalized[:self._context_dim]
        
        # Create time grid (dimensional)
        t_dimensional = np.arange(t_start, t_end + dt, dt)
        N = len(t_dimensional)
        
        # Convert to nondimensional
        t_nondim = t_dimensional / self._scales.T
        
        # Convert to tensors
        t_tensor = torch.tensor(t_nondim, dtype=torch.float32).unsqueeze(-1)  # [N, 1]
        context_tensor = torch.tensor(context_normalized, dtype=torch.float32)  # [context_dim]
        
        # Run inference
        device = next(self._model.parameters()).device
        t_tensor = t_tensor.to(device)
        context_tensor = context_tensor.to(device)
        
        with torch.no_grad():
            # Model forward returns (state, physics_residuals) for DirectionANPINN
            result = self._model(t_tensor, context_tensor)
            if isinstance(result, tuple):
                state_nondim = result[0]  # Extract state from tuple
            else:
                state_nondim = result
            
            # Handle batching
            if state_nondim.dim() == 3:
                state_nondim = state_nondim.squeeze(0)  # Remove batch dimension
            
            state_nondim = state_nondim.cpu().numpy()  # [N, 14]
        
        # Denormalize state
        state_dimensional = state_nondim.copy()
        state_dimensional[:, 0:3] *= self._scales.L      # Position [x, y, z] → meters
        state_dimensional[:, 3:6] *= self._scales.V      # Velocity [vx, vy, vz] → m/s
        state_dimensional[:, 10:13] *= self._scales.W     # Angular velocity [wx, wy, wz] → rad/s
        state_dimensional[:, 13] *= self._scales.M       # Mass [m] → kg
        # Quaternion [q0, q1, q2, q3] is already dimensionless
        
        return t_dimensional, state_dimensional
    
    def get_model_info(self) -> Dict:
        """Get model information"""
        if self._model is None:
            return {'loaded': False}
        
        return {
            'loaded': True,
            'model_type': self._config.get('model', {}).get('type', 'unknown'),
            'context_dim': self._context_dim,
            'scales': {
                'L': self._scales.L,
                'V': self._scales.V,
                'T': self._scales.T,
                'M': self._scales.M,
                'F': self._scales.F,
                'W': self._scales.W
            }
        }


# Singleton instance
_ml_model_service = None

def get_ml_model_service() -> MLModelService:
    """Get singleton ML model service instance"""
    global _ml_model_service
    if _ml_model_service is None:
        _ml_model_service = MLModelService()
    return _ml_model_service

