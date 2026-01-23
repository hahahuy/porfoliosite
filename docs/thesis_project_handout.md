# Physics Informed Learning for Rocket Dynamics

## Overview

This repository contains an undergraduate research project exploring **physics informed and data driven modeling of rocket flight dynamics**.
The work investigates how neural networks can learn system behavior while explicitly respecting known physical laws.

The project sits at the intersection of:

* Classical mechanics and rocket dynamics
* Machine learning and neural networks
* Physics Informed Neural Networks (PINNs)

The primary objective is to build models that are both **accurate** and **physically consistent**, serving as fast surrogate models for simulation and analysis.

---

## Motivation

Traditional rocket trajectory simulation relies on analytical equations solved numerically.
While accurate, these approaches can be computationally heavy and difficult to integrate into learning based pipelines.

Pure data driven models, on the other hand, are flexible but often violate physical constraints.

This project explores a hybrid approach where:

* Physical laws guide the learning process
* Neural networks approximate system dynamics
* Learned models remain consistent with mechanics such as kinematics and force balance

---

## Core Ideas

The repository focuses on:

* Learning rocket motion from simulated or generated data
* Embedding physics constraints directly into loss functions
* Enforcing relationships such as:

  * Position velocity consistency
  * Velocity acceleration consistency
  * Physically meaningful state evolution
* Comparing physics informed models with purely data driven baselines

---

## Project Structure

A high level overview of the repository:

* `src/`
  Core implementation including physics equations, neural network models, and loss functions

* `configs/`
  YAML configuration files defining model architecture, training settings, and experiment parameters

* `data/`
  Datasets used for training and evaluation, typically generated through simulation

* `experiments/` or `runs/`
  Training outputs, logs, metrics, and evaluation results

* `docs/`
  Supplementary notes, figures, or thesis related material

Each experiment is designed to be reproducible and configurable through independent config files.

---

## Datasets

### Dataset Structure

The project uses **HDF5 format** for processed datasets. Each dataset file contains:

**Location**: `data/processed/` (v1) or `data/processed_v2/` (v2)

**File Structure**:
- `train.h5`, `val.h5`, `test.h5` - Separate files for train/validation/test splits

**HDF5 Schema**:
```
train.h5 (or val.h5, test.h5)
├── inputs/
│   ├── t: [n_cases, N]                    # Time grid (nondimensional)
│   └── context: [n_cases, context_dim]    # Context parameters (normalized)
├── targets/
│   └── state: [n_cases, N, 14]           # State trajectories (nondimensional)
└── meta/
    ├── scales: JSON string                # Reference scales (L, V, T, M, F, W)
    └── context_fields: JSON array        # Context field names
```

**Dimensions**:
- `n_cases`: Number of trajectory cases (typically 120 train, 20 val, 20 test)
- `N`: Number of time points per trajectory (typically 1501 for 30s at 50Hz)
- `context_dim`: Dimension of context vector (varies, typically 7-22 fields)

### State Format (14-Dimensional)

The model predicts a **14-dimensional state vector** at each time step:

| Index | Variable | Symbol | Description | Units (Dimensional) |
|-------|----------|--------|-------------|---------------------|
| 0-2 | Position | `[x, y, z]` | 3D position coordinates | meters (m) |
| 3-5 | Velocity | `[vx, vy, vz]` | 3D velocity components | meters/second (m/s) |
| 6-9 | Quaternion | `[q0, q1, q2, q3]` | Attitude quaternion (unit quaternion) | dimensionless |
| 10-12 | Angular Velocity | `[wx, wy, wz]` | Angular velocity components | radians/second (rad/s) |
| 13 | Mass | `m` | Rocket mass | kilograms (kg) |

**Important**: All states in the dataset are **nondimensionalized** using reference scales. See [Normalization](#normalization-and-scaling) section below.

### Context Parameters

The context vector encodes scenario-specific physical parameters. The canonical field order is:

| Index | Parameter | Symbol | Unit | Description | Typical Range |
|-------|----------|--------|------|-------------|---------------|
| 0 | Initial mass | `m0` | kg | Initial rocket mass | [45, 65] |
| 1 | Specific impulse | `Isp` | s | Propellant efficiency | [220, 280] |
| 2 | Drag coefficient | `Cd` | - | Drag coefficient | [0.25, 0.45] |
| 3 | Lift curve slope | `CL_alpha` | 1/rad | Lift coefficient per unit angle of attack | [2.5, 4.5] |
| 4 | Pitch moment coefficient | `Cm_alpha` | 1/rad | Pitch moment coefficient per unit angle of attack | [-1.2, -0.4] |
| 5 | Reference area | `S` | m² | Reference area for aerodynamic forces | varies |
| 6 | Reference length | `l_ref` | m | Reference length for moments | ~1.2 |
| 7 | Maximum thrust | `Tmax` | N | Maximum available thrust | [3000, 5000] |
| 8 | Dry mass | `mdry` | kg | Minimum mass after fuel depletion | varies |
| 9 | Maximum gimbal angle | `gimbal_max_rad` | rad | Maximum gimbal deflection | varies |
| 10 | Thrust rate | `thrust_rate` | N/s | Maximum thrust change rate | varies |
| 11 | Gimbal rate | `gimbal_rate_rad` | rad/s | Maximum gimbal angular velocity | varies |
| 12-14 | Moments of inertia | `Ix, Iy, Iz` | kg⋅m² | Principal moments of inertia | varies |
| 15 | Sea level density | `rho0` | kg/m³ | Atmospheric density at sea level | ~1.225 |
| 16 | Atmospheric scale height | `H` | m | Exponential atmosphere scale height | ~8500 |
| 17 | Wind magnitude | `wind_mag` | m/s | Wind speed magnitude | [0, 15] |
| 18 | Wind direction | `wind_dir_rad` | rad | Wind direction angle | [0, 2π] |
| 19 | Gust amplitude | `gust_amp` | m/s | Gust amplitude | varies |
| 20 | Gust frequency | `gust_freq` | Hz | Gust frequency | varies |
| 21 | Maximum dynamic pressure | `qmax` | Pa | Maximum allowable dynamic pressure | varies |
| 22 | Maximum load factor | `nmax` | g | Maximum normal load factor | varies |

**Note**: Only fields present in the raw data are included. Missing fields are set to 0.0 in the normalized context vector.

### Normalization and Scaling

All inputs and outputs use **physics-aware nondimensionalization** based on reference scales:

**Reference Scales** (from `configs/scales.yaml`):
- `L = 10000.0` m (characteristic length, target altitude)
- `V = 313.0` m/s (characteristic velocity, ≈ √(g₀ × L))
- `T = 31.62` s (characteristic time, ≈ L / V)
- `M = 50.0` kg (characteristic mass, nominal wet mass)
- `F = 490.0` N (characteristic force, ≈ M × g₀)
- `W = 0.0316` 1/s (angular rate scale, = 1 / T)

**Nondimensionalization Rules**:
- **Position** `[x, y, z]`: Divide by `L`
- **Velocity** `[vx, vy, vz]`: Divide by `V`
- **Time** `t`: Divide by `T`
- **Mass** `m`: Divide by `M`
- **Angular velocity** `[wx, wy, wz]`: Divide by `W`
- **Thrust** `T`: Divide by `F`

**Context Normalization**:
- **Mass parameters** (`m0`, `mdry`): Normalized by `M`
- **Force parameters** (`Tmax`): Normalized by `F`
- **Inertia parameters** (`Ix`, `Iy`, `Iz`): Normalized by `M × l_ref²`
- **Area parameters** (`S`): Normalized by `l_ref²`
- **Velocity parameters** (`wind_mag`, `gust_amp`): Normalized by `V`
- **Frequency parameters** (`gust_freq`): Multiplied by `T`
- **Dimensionless parameters** (`Cd`, `CL_alpha`, `Cm_alpha`, `nmax`): Already O(1), kept as-is
- **Special parameters**:
  - `Isp`: Normalized by reference value (250.0 s)
  - `rho0`: Normalized by sea level density (1.225 kg/m³)
  - `H`: Normalized by reference scale height (8500.0 m)

**Implementation**: See `src/data/preprocess.py` - `build_context_vector()` and `to_nd()` functions.

---

## Model Input and Output

### Model Interface

All models follow a consistent interface:

```python
def forward(
    self,
    t: torch.Tensor,           # Time grid [batch, N, 1] or [N, 1] (nondimensional)
    context: torch.Tensor      # Context vector [batch, context_dim] or [context_dim] (normalized)
) -> torch.Tensor:
    """
    Returns:
        state: Predicted state [batch, N, 14] or [N, 14] (nondimensional)
    """
```

**Convenience Method**:
```python
def predict_trajectory(
    self,
    t: torch.Tensor,           # Time grid [N] (nondimensional)
    context: torch.Tensor       # Context vector [context_dim] (normalized)
) -> torch.Tensor:
    """
    Returns:
        state: Trajectory [N, 14] (nondimensional)
    """
```

### Input Requirements

**Time Grid (`t`)**:
- **Shape**: `[N]` (1D) or `[batch, N, 1]` (3D) or `[N, 1]` (2D)
- **Type**: `torch.float32`
- **Units**: Nondimensional time (dimensional time / T_scale)
- **Range**: Typically `[0, ~0.95]` for 30-second trajectories
- **Format**: Uniform or non-uniform time grid (model handles both)

**Context Vector (`context`)**:
- **Shape**: `[context_dim]` (1D) or `[batch, context_dim]` (2D)
- **Type**: `torch.float32`
- **Units**: Normalized using physics-aware scaling (see above)
- **Required Fields**: Depends on model, but typically includes `m0`, `Isp`, `Cd`, `CL_alpha`, `Cm_alpha`, `Tmax`, `wind_mag`
- **Missing Fields**: Set to 0.0 in normalized vector

### Output Format

**State Trajectory (`state`)**:
- **Shape**: `[N, 14]` (single trajectory) or `[batch, N, 14]` (batched)
- **Type**: `torch.float32`
- **Units**: Nondimensional (must be converted back to dimensional units)
- **Order**: `[x, y, z, vx, vy, vz, q0, q1, q2, q3, wx, wy, wz, m]`

**Important**: Outputs are **nondimensional** and must be converted to dimensional units using the scales.

---

## API Integration Guide

### Loading a Trained Model

**Step 1: Load Checkpoint**
```python
import torch
from src.models import create_model
from src.data.preprocess import load_scales
from src.data.preprocess import build_context_vector, CONTEXT_FIELDS
from src.data.preprocess import Scales

# Load checkpoint
checkpoint_path = "experiments/exp15_02_12_direction_an_baseline/checkpoints/best.pt"
checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
model_state = checkpoint["model_state_dict"]

# Load scales
scales_path = "configs/scales.yaml"
scales = load_scales(scales_path)  # Returns Scales(L, V, T, M, F, W)

# Load model config (from checkpoint's experiment directory)
import yaml
config_path = "experiments/exp15_02_12_direction_an_baseline/logs/config.yaml"
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# Create model
model_cfg = config["model"]
context_dim = 7  # Or load from dataset: train_loader.dataset.context_dim
model = create_model(model_cfg, context_dim)
model.load_state_dict(model_state)
model.eval()  # Set to evaluation mode
```

### Preparing Inputs for Inference

**Step 2: Prepare Time Grid**
```python
import numpy as np
import torch

# Create time grid (dimensional, in seconds)
t_start = 0.0
t_end = 30.0
dt = 0.02  # 50 Hz
t_dimensional = np.arange(t_start, t_end + dt, dt)  # [N] seconds

# Convert to nondimensional
t_nondim = t_dimensional / scales.T  # [N] nondimensional
t_tensor = torch.tensor(t_nondim, dtype=torch.float32).unsqueeze(-1)  # [N, 1]
```

**Step 3: Prepare Context Vector**
```python
# Define physical parameters (dimensional units)
params = {
    "m0": 55.0,           # kg
    "Isp": 250.0,         # s
    "Cd": 0.35,           # dimensionless
    "CL_alpha": 3.5,      # 1/rad
    "Cm_alpha": -0.8,     # 1/rad
    "Tmax": 4000.0,       # N
    "wind_mag": 5.0,      # m/s
    # ... other parameters as needed
}

# Build normalized context vector
context_fields = ["m0", "Isp", "Cd", "CL_alpha", "Cm_alpha", "Tmax", "wind_mag"]
context_normalized = build_context_vector(params, scales, fields=context_fields)
context_tensor = torch.tensor(context_normalized, dtype=torch.float32)  # [context_dim]
```

### Running Inference

**Step 4: Generate Prediction**
```python
# Single trajectory prediction
with torch.no_grad():
    state_nondim = model.predict_trajectory(t_tensor, context_tensor)  # [N, 14]

# Or use forward for batched predictions
batch_t = t_tensor.unsqueeze(0)  # [1, N, 1]
batch_context = context_tensor.unsqueeze(0)  # [1, context_dim]
with torch.no_grad():
    state_nondim_batch = model.forward(batch_t, batch_context)  # [1, N, 14]
    state_nondim = state_nondim_batch.squeeze(0)  # [N, 14]
```

### Converting Outputs to Dimensional Units

**Step 5: Denormalize State**
```python
import numpy as np

# Convert to numpy
state_nondim_np = state_nondim.numpy()  # [N, 14]

# Denormalize using scales
state_dimensional = state_nondim_np.copy()
state_dimensional[:, 0:3] *= scales.L      # Position [x, y, z] → meters
state_dimensional[:, 3:6] *= scales.V      # Velocity [vx, vy, vz] → m/s
state_dimensional[:, 10:13] *= scales.W   # Angular velocity [wx, wy, wz] → rad/s
state_dimensional[:, 13] *= scales.M      # Mass [m] → kg
# Quaternion [q0, q1, q2, q3] is already dimensionless

# Denormalize time
t_dimensional = t_nondim * scales.T  # seconds
```

### Complete API Example

```python
import torch
import numpy as np
from src.models import create_model
from src.data.preprocess import load_scales, build_context_vector
import yaml

def predict_rocket_trajectory(
    checkpoint_path: str,
    config_path: str,
    scales_path: str,
    params: dict,
    t_start: float = 0.0,
    t_end: float = 30.0,
    dt: float = 0.02
) -> dict:
    """
    Predict rocket trajectory for given parameters.
    
    Args:
        checkpoint_path: Path to model checkpoint (.pt file)
        config_path: Path to model config YAML
        scales_path: Path to scales YAML
        params: Dictionary of physical parameters (dimensional units)
        t_start: Start time in seconds
        t_end: End time in seconds
        dt: Time step in seconds
    
    Returns:
        Dictionary with:
            - 'time': [N] time array (seconds)
            - 'state': [N, 14] state array (dimensional units)
            - 'state_names': List of state variable names
    """
    # Load model
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    scales = load_scales(scales_path)
    
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    model_cfg = config["model"]
    context_dim = len(params)  # Adjust based on your context fields
    model = create_model(model_cfg, context_dim)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    
    # Prepare inputs
    t_dimensional = np.arange(t_start, t_end + dt, dt)
    t_nondim = t_dimensional / scales.T
    t_tensor = torch.tensor(t_nondim, dtype=torch.float32).unsqueeze(-1)
    
    context_fields = list(params.keys())
    context_normalized = build_context_vector(params, scales, fields=context_fields)
    context_tensor = torch.tensor(context_normalized, dtype=torch.float32)
    
    # Predict
    with torch.no_grad():
        state_nondim = model.predict_trajectory(t_tensor, context_tensor)
    
    # Denormalize
    state_dimensional = state_nondim.numpy().copy()
    state_dimensional[:, 0:3] *= scales.L
    state_dimensional[:, 3:6] *= scales.V
    state_dimensional[:, 10:13] *= scales.W
    state_dimensional[:, 13] *= scales.M
    
    return {
        'time': t_dimensional,
        'state': state_dimensional,
        'state_names': ['x', 'y', 'z', 'vx', 'vy', 'vz', 'q0', 'q1', 'q2', 'q3', 'wx', 'wy', 'wz', 'm']
    }

# Usage example
params = {
    "m0": 55.0,
    "Isp": 250.0,
    "Cd": 0.35,
    "CL_alpha": 3.5,
    "Cm_alpha": -0.8,
    "Tmax": 4000.0,
    "wind_mag": 5.0,
}

result = predict_rocket_trajectory(
    checkpoint_path="experiments/exp15_02_12_direction_an_baseline/checkpoints/best.pt",
    config_path="experiments/exp15_02_12_direction_an_baseline/logs/config.yaml",
    scales_path="configs/scales.yaml",
    params=params
)

# Access results
time = result['time']  # [N] seconds
position = result['state'][:, 0:3]  # [N, 3] meters
velocity = result['state'][:, 3:6]  # [N, 3] m/s
quaternion = result['state'][:, 6:10]  # [N, 4] unit quaternion
angular_velocity = result['state'][:, 10:13]  # [N, 3] rad/s
mass = result['state'][:, 13]  # [N] kg
```

### Important Notes for API Integration

1. **Normalization is Critical**: All inputs must be normalized and outputs must be denormalized using the scales. Incorrect scaling will produce incorrect results.

2. **Context Field Order**: The context vector must match the order expected by the model. Use `CONTEXT_FIELDS` from `src/data/preprocess.py` or check the dataset's `meta/context_fields` in the HDF5 file.

3. **Device Handling**: Models can run on CPU or GPU. Use `model.to(device)` before inference if needed.

4. **Batch Processing**: For multiple trajectories, batch the inputs:
   ```python
   batch_t = torch.stack([t1, t2, t3], dim=0)  # [3, N, 1]
   batch_context = torch.stack([ctx1, ctx2, ctx3], dim=0)  # [3, context_dim]
   state_batch = model.forward(batch_t, batch_context)  # [3, N, 14]
   ```

5. **Model Variants**: Different model architectures (PINN, LatentODE, Sequence, Hybrid) all follow the same interface but may have different performance characteristics.

6. **Checkpoint Structure**: Checkpoints contain:
   - `model_state_dict`: Model weights
   - `epoch`: Training epoch
   - `loss`: Validation loss
   - Other training metadata

---

## Physics Informed Training

Instead of minimizing prediction error alone, training incorporates additional constraints derived from physics, such as:

* Time derivatives matching known kinematic relationships
* Consistency between predicted states
* Optional smoothness or regularization terms

This reduces unphysical behavior and improves generalization.

---

## Intended Audience

This repository is intended for:

* Undergraduate and graduate students in ML, aerospace, or applied physics
* Researchers interested in PINNs or hybrid modeling
* Reviewers evaluating academic work
* Developers looking for reference implementations of physics based losses

Basic familiarity with Python, neural networks, and classical mechanics is recommended.

---

## Getting Started

Suggested approach for new readers:

1. Read through this README
2. Inspect a single configuration file in `configs/`
3. Explore the corresponding model and loss implementation
4. Review experiment results before moving to advanced variants

The project is experimental and iterative by design.

---

## Research Context

This repository is part of an undergraduate thesis project.
Code clarity and experimental flexibility are prioritized over production level optimization.

Multiple experimental directions may coexist to reflect the research process.
