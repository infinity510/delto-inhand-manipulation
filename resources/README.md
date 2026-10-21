# Research Literature & Academic References (`resources/`)

This directory archives foundational research literature, scientific papers, and theoretical notes that underpin the algorithmic architecture and physical modeling of this project.

---

## Directory Organization

```
resources/
├── papers/                              # Peer-reviewed research papers & preprints
│   ├── 1808.00177v5.pdf                 # OpenAI Dactyl: Learning Dexterous In-Hand Manipulation
│   ├── 2210.04887v1.pdf                 # AnyTeleop: A General Vision-Based Teleoperation System
│   ├── Dexterous_Manipulation_...pdf    # Dexterous Manipulation with Deep RL: Efficient & General
│   └── p49.pdf                          # Foundational robotic grasping & in-hand kinematics
└── notes/                               # Educational & mathematical references
    └── reinforcement-learning-notes.pdf # Deep reinforcement learning, PPO & GAE foundations
```

---

## Summary of Reference Literature

1. **OpenAI Dactyl (`1808.00177v5.pdf`)**:
   - *Title*: Learning Dexterous In-Hand Manipulation
   - *Key Insights Utilized*: Sim-to-Real Domain Randomization on non-privilege observations, goal resampling protocol, exponential observation noise modeling, and sensor latency FIFO queues.

2. **AnyTeleop (`2210.04887v1.pdf`)**:
   - *Title*: AnyTeleop: A General Vision-Based Dexterous Robot Teleoperation System
   - *Key Insights Utilized*: Single-camera marker-based hand pose tracking, relaxed-hand calibration anchors, and real-time IK joint retargeting.

3. **Dexterous Manipulation with Deep RL (`Dexterous_Manipulation_with_Deep_Reinforcement_Learning_Efficient_General_and_Low-Cost.pdf`)**:
   - *Key Insights Utilized*: Natural curriculum progression, multi-finger gaiting rewards, and contact friction bounds.

4. **Deep Reinforcement Learning Notes (`reinforcement-learning-notes.pdf`)**:
   - *Key Insights Utilized*: PPO clipped surrogate objective, Generalized Advantage Estimation ($\text{GAE}(\gamma, \lambda)$), Huber value loss formulation, and orthogonal weight initialization.
