# Demonstration Datasets (`data/`)

This directory contains human teleoperation demonstration datasets for 3D in-hand dexterous reorientation on the 12-DOF Delto Gripper-3F.

---

## Directory Organization

```
data/
├── raw/         # Raw demonstration episodes recorded from live teleoperation
│   ├── cube_*.hdf5       # Cube demonstrations (45mm edge length, 1.0kg)
│   ├── cuboid_*.hdf5     # Cuboid demonstrations (45mm x 45mm x 70mm, 1.0kg)
│   └── cylinder_*.hdf5   # Cylinder demonstrations (45mm diameter x 70mm height, 1.0kg)
└── processed/   # Cleaned, dead-time trimmed, and velocity-smoothed episodes
    ├── cube_*.hdf5
    ├── cuboid_*.hdf5
    └── cylinder_*.hdf5
```

---

## Dataset Schema & Modalities

Each `.hdf5` file corresponds to an individual in-hand manipulation trajectory sampled at $50\text{ Hz}$ ($20\text{ ms}$ control timesteps):

| HDF5 Dataset Key | Shape | Type | Description |
| :--- | :---: | :---: | :--- |
| `robot_qpos` | `(T, 12)` | `float32` | Joint angular positions (radians) for all 12 revolute finger joints |
| `robot_qvel` | `(T, 12)` | `float32` | Joint angular velocities ($\text{rad/s}$) from finite-difference encoders |
| `object_pos` | `(T, 3)` | `float32` | 3D Cartesian position $[x, y, z]$ of object in palm frame (meters) |
| `object_quat` | `(T, 4)` | `float32` | Object orientation quaternion $[w, x, y, z]$ in MuJoCo convention |
| `action` | `(T, 12)` | `float32` | Desired PD position targets dispatched to finger actuators |

### Episode Metadata Attributes
- `f.attrs['object_id']`: Integer identifier (`1` = Cylinder, `2` = Cube, `3` = Cuboid).
- `f.attrs['target_quat']`: 4D unit quaternion $[w, x, y, z]$ representing the Hindsight Experience Replay (HER) labeled goal orientation.

---

## Pipeline Operations

### 1. Data Collection
Collect raw human demonstrations using webcam ArUco tracking:
```bash
python3 src/teleoperation/collect_data.py
```

### 2. Quality Inspection
Audit recorded trajectories for drops, object translation, and actuator jerk:
```bash
python3 src/teleoperation/inspect_data.py data/processed
```

### 3. Preprocessing & Dead-Time Trimming
Trim static idling frames at the start/end of episodes:
```bash
python3 src/teleoperation/preprocess_data.py --input_dir data/raw --output_dir data/processed
```

### 4. Interactive Replay
Watch recorded trajectories replayed in the MuJoCo 3D viewer:
```bash
python3 src/teleoperation/replay_data.py
```
