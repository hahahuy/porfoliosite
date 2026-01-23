"""ML API routes for project demos"""
from flask import Blueprint, request, jsonify, abort, current_app
from app.services.content_service import ContentService
from app.services.ml_model_service import get_ml_model_service

ml_api_bp = Blueprint('ml_api', __name__, url_prefix='/api/ml')


@ml_api_bp.route('/projects/<int:project_id>/predict', methods=['POST'])
def predict(project_id):
    """
    ML prediction endpoint for a specific project.
    
    This endpoint handles inference requests for ML demos associated with projects.
    Each project can have its own ML model implementation.
    
    Expected request body (JSON):
    {
        "data": {...}  # Model-specific input data
    }
    
    Returns:
        JSON response with prediction results
    """
    try:
        # Verify project exists
        content_service = ContentService(current_app.config)
        project = content_service.get_project_by_id(project_id)
        
        if not project:
            return jsonify({
                'error': 'Project not found',
                'project_id': project_id
            }), 404
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No data provided',
                'project_id': project_id
            }), 400
        
        # Project-specific implementations
        if project_id == 1:
            # Rocket Dynamics Prediction using PINN model
            return _predict_rocket_dynamics_pinn(data.get('data', {}))
        else:
            # Generic placeholder for other projects
            current_app.logger.info(f"ML prediction request for project {project_id}")
            return jsonify({
                'project_id': project_id,
                'project_title': project.get('title'),
                'status': 'not_implemented',
                'message': 'ML inference not yet implemented for this project',
                'received_data': data
            }), 501  # Not Implemented
        
    except Exception as e:
        current_app.logger.error(f"Error in ML prediction for project {project_id}: {e}")
        return jsonify({
            'error': 'Internal server error',
            'project_id': project_id,
            'message': str(e)
        }), 500


def _predict_rocket_dynamics_pinn(input_data):
    """
    Predict rocket trajectory using trained Physics Informed Neural Network (PINN).
    
    Input format:
    {
        "m0": float,              # Initial mass (kg)
        "Isp": float,             # Specific impulse (s)
        "Cd": float,              # Drag coefficient
        "CL_alpha": float,        # Lift curve slope (1/rad)
        "Cm_alpha": float,        # Pitch moment coefficient (1/rad)
        "Tmax": float,            # Maximum thrust (N)
        "wind_mag": float,        # Wind magnitude (m/s)
        "t_start": float,         # Start time (s) - optional, default 0.0
        "t_end": float,           # End time (s) - optional, default 30.0
        "dt": float               # Time step (s) - optional, default 0.02
    }
    """
    try:
        # Get ML model service
        ml_service = get_ml_model_service()
        
        # Load model if not already loaded
        if not ml_service.load_model(project_id=1):
            return jsonify({
                'error': 'Model not available',
                'message': 'Failed to load ML model'
            }), 503
        
        # Extract parameters
        params = {
            'm0': float(input_data.get('m0', 55.0)),
            'Isp': float(input_data.get('Isp', 250.0)),
            'Cd': float(input_data.get('Cd', 0.35)),
            'CL_alpha': float(input_data.get('CL_alpha', 3.5)),
            'Cm_alpha': float(input_data.get('Cm_alpha', -0.8)),
            'Tmax': float(input_data.get('Tmax', 4000.0)),
            'wind_mag': float(input_data.get('wind_mag', 5.0)),
        }
        
        # Time parameters
        t_start = float(input_data.get('t_start', 0.0))
        t_end = float(input_data.get('t_end', 30.0))
        dt = float(input_data.get('dt', 0.02))
        
        # Run prediction
        time_array, state_array = ml_service.predict(
            params=params,
            t_start=t_start,
            t_end=t_end,
            dt=dt
        )
        
        # Convert to trajectory format
        # State format: [x, y, z, vx, vy, vz, q0, q1, q2, q3, wx, wy, wz, m]
        trajectory = []
        for i in range(len(time_array)):
            trajectory.append({
                'time': float(time_array[i]),
                'position': {
                    'x': float(state_array[i, 0]),
                    'y': float(state_array[i, 1]),
                    'z': float(state_array[i, 2])
                },
                'velocity': {
                    'x': float(state_array[i, 3]),
                    'y': float(state_array[i, 4]),
                    'z': float(state_array[i, 5])
                },
                'quaternion': {
                    'q0': float(state_array[i, 6]),
                    'q1': float(state_array[i, 7]),
                    'q2': float(state_array[i, 8]),
                    'q3': float(state_array[i, 9])
                },
                'angular_velocity': {
                    'wx': float(state_array[i, 10]),
                    'wy': float(state_array[i, 11]),
                    'wz': float(state_array[i, 12])
                },
                'mass': float(state_array[i, 13])
            })
        
        return jsonify({
            'project_id': 1,
            'status': 'success',
            'trajectory': trajectory,
            'final_position': trajectory[-1]['position'] if trajectory else None,
            'final_velocity': trajectory[-1]['velocity'] if trajectory else None,
            'final_mass': trajectory[-1]['mass'] if trajectory else None,
            'simulation_params': {
                't_start': t_start,
                't_end': t_end,
                'dt': dt,
                'total_time': t_end - t_start,
                'num_points': len(trajectory)
            }
        }), 200
        
    except (KeyError, ValueError, TypeError) as e:
        current_app.logger.error(f"Error in prediction: {e}", exc_info=True)
        return jsonify({
            'error': 'Invalid input data',
            'message': str(e),
            'required_fields': {
                'm0': 'Initial mass (kg)',
                'Isp': 'Specific impulse (s)',
                'Cd': 'Drag coefficient',
                'CL_alpha': 'Lift curve slope (1/rad)',
                'Cm_alpha': 'Pitch moment coefficient (1/rad)',
                'Tmax': 'Maximum thrust (N)',
                'wind_mag': 'Wind magnitude (m/s)',
                't_start': 'Start time (s) - optional',
                't_end': 'End time (s) - optional',
                'dt': 'Time step (s) - optional'
            }
        }), 400
    except Exception as e:
        current_app.logger.error(f"Unexpected error in prediction: {e}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@ml_api_bp.route('/projects/<int:project_id>/health', methods=['GET'])
def ml_health(project_id):
    """
    Health check endpoint for ML model associated with a project.
    
    Returns:
        JSON response indicating if the ML model is ready
    """
    try:
        # Verify project exists
        content_service = ContentService(current_app.config)
        project = content_service.get_project_by_id(project_id)
        
        if not project:
            return jsonify({
                'error': 'Project not found',
                'project_id': project_id
            }), 404
        
        # Check if ML model is loaded and ready
        if project_id == 1:
            ml_service = get_ml_model_service()
            model_loaded = ml_service.load_model(project_id)
            model_info = ml_service.get_model_info() if model_loaded else {}
            
            return jsonify({
                'project_id': project_id,
                'project_title': project.get('title'),
                'status': 'ready' if model_loaded else 'not_loaded',
                'ready': model_loaded,
                'model_info': model_info
            }), 200
        else:
            return jsonify({
                'project_id': project_id,
                'project_title': project.get('title'),
                'status': 'not_implemented',
                'message': 'ML model health check not yet implemented for this project',
                'ready': False
            }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error in ML health check for project {project_id}: {e}")
        return jsonify({
            'error': 'Internal server error',
            'project_id': project_id
        }), 500


@ml_api_bp.route('/projects/<int:project_id>/info', methods=['GET'])
def ml_info(project_id):
    """
    Get information about the ML model for a specific project.
    
    Returns:
        JSON response with model metadata
    """
    try:
        # Verify project exists
        content_service = ContentService(current_app.config)
        project = content_service.get_project_by_id(project_id)
        
        if not project:
            return jsonify({
                'error': 'Project not found',
                'project_id': project_id
            }), 404
        
        # Return actual model information
        if project_id == 1:
            ml_service = get_ml_model_service()
            model_info = ml_service.get_model_info()
            
            return jsonify({
                'project_id': project_id,
                'project_title': project.get('title'),
                'tags': project.get('tags', []),
                'model_info': model_info,
                'model_details': project.get('model_info', {}),
                'endpoints': {
                    'predict': f'/api/ml/projects/{project_id}/predict',
                    'health': f'/api/ml/projects/{project_id}/health'
                },
                'input_format': {
                    'm0': 'Initial mass (kg)',
                    'Isp': 'Specific impulse (s)',
                    'Cd': 'Drag coefficient',
                    'CL_alpha': 'Lift curve slope (1/rad)',
                    'Cm_alpha': 'Pitch moment coefficient (1/rad)',
                    'Tmax': 'Maximum thrust (N)',
                    'wind_mag': 'Wind magnitude (m/s)',
                    't_start': 'Start time (s) - optional',
                    't_end': 'End time (s) - optional',
                    'dt': 'Time step (s) - optional'
                },
                'output_format': {
                    'trajectory': 'Array of state vectors',
                    'state_dimension': 14,
                    'state_components': ['x', 'y', 'z', 'vx', 'vy', 'vz', 'q0', 'q1', 'q2', 'q3', 'wx', 'wy', 'wz', 'm']
                }
            }), 200
        else:
            return jsonify({
                'project_id': project_id,
                'project_title': project.get('title'),
                'tags': project.get('tags', []),
                'status': 'not_implemented',
                'message': 'ML model info not yet implemented for this project',
                'endpoints': {
                    'predict': f'/api/ml/projects/{project_id}/predict',
                    'health': f'/api/ml/projects/{project_id}/health'
                }
            }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting ML info for project {project_id}: {e}")
        return jsonify({
            'error': 'Internal server error',
            'project_id': project_id
        }), 500

