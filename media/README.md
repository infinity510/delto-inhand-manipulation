# Demonstration Media (`media/`)

This directory contains visual demonstrations, simulation capture videos, and training convergence plots.

---

## Directory Organization

```
media/
├── plots/
│   └── training_accuracy.png             # Historical accuracy and milestone progression plot
└── videos/
    ├── stage1_nominal_dexterity.mp4      # High-fidelity video of Stage 1 nominal reorientations
    └── stage2_large_angle_gaiting.mp4    # Video showcasing Stage 2 large-angle in-hand finger gaiting
```

---

## Media Overview

### 1. Stage 1 Nominal Dexterity (`stage1_nominal_dexterity.mp4`)
- **Focus**: Precision multi-finger reorientations across the small-to-medium envelope ($10^\circ \text{ to } 40^\circ$).
- **Features**: Smooth silicone contact dynamics, stable tripod cradling, and sub-degree terminal alignment.

### 2. Stage 2 Large-Angle Dynamic Gaiting (`stage2_large_angle_gaiting.mp4`)
- **Focus**: Continuous multi-finger dynamic in-hand gaiting across extreme angles ($40^\circ \text{ to } 90^\circ$).
- **Features**: Asymmetric finger re-engagement, distal knuckle anti-clench compliance, and zero palm hearth intrusions.

### 3. Training Accuracy Progression (`training_accuracy.png`)
- **Telemetry**: Empirical success rate curves, policy entropy decay, Huber critic value loss convergence, and domain randomization robustness milestones.
