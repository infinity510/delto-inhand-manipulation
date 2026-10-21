# Evaluation Benchmarks & Telemetry Reports (`evaluation/`)

This directory houses the comprehensive performance evaluations, benchmark reports, and multi-stage training progression telemetry for the Delto-3F in-hand manipulation framework.

---

## Directory Organization

```
evaluation/
├── README.md               # Benchmark documentation & protocol specifications
└── reports/                # Standardized evaluation markdown reports
    ├── EVALUATION_DR_REPORT.md             # Primary Sim-to-Real Domain Randomization report
    ├── EVALUATION_REPORT.md                # Nominal clean baseline benchmark report
    ├── EVALUATION_DR_FULL_REPORT.md        # Extended multi-seed DR evaluation report
    ├── EVALUATION_DR_REPORT_CLEAN.md       # Baseline presentation comparison report
    ├── EVALUATION_DR_REPORT_PREV_PEAK.md   # Prior peak champion comparison
    └── OVERNIGHT_PROGRESS_REPORT.md        # Comprehensive multi-stage curriculum progression
```

> **Note**: For backward compatibility with legacy command flags (`--report_file EVAL/...`), `EVAL` at the repository root is maintained as an active symlink pointing to `evaluation/reports`.

---

## Standard Benchmark Protocol

The canonical benchmark consists of **600 stratified evaluation episodes** distributed evenly:
- **Objects**: Cube (45mm), Cylinder (45mm x 70mm), Cuboid (45mm x 45mm x 70mm) — 200 episodes each.
- **Orientation Ranges**:
  - **Range 1 ($10^\circ \text{ to } 40^\circ$)**: Small-to-medium reorientations (precision alignment).
  - **Range 2 ($40^\circ \text{ to } 90^\circ$)**: Large-angle dynamic in-hand gaiting trajectories.
- **Workers**: 16 parallel CPU environments.
- **Tolerance**: 10.0% relative orientation error threshold ($\epsilon = 0.10$).

### Core Benchmark Metrics
1. **Success Rate (@10% Error)**: Percentage of episodes achieving orientation error $\le 10\%$ of initial geodesic distance within step budget.
2. **Mean Rotational Closure**: $1 - (d_{\theta, \text{final}} / d_{\theta, 0})$, measuring percentage of target rotation completed.
3. **Pre-Goal Object Retention Rate**: Percentage of episodes retaining the object without dropping prior to goal achievement.
4. **Effective Manipulation Index (EMI)**: Composite metric defined as $\text{Success Rate} \times \text{Rotational Closure}$.
5. **Composite Benchmark Score**: Multi-objective index combining EMI, final precision, and stability.

---

## Running Benchmarks

### 1. High-Throughput Sim-to-Real Domain Randomization Benchmark
```bash
python3 in_hand_manipulation/evaluate_dr.py \
  --checkpoint models/best_model_with_dr.pth \
  --episodes_per_range 100 \
  --num_workers 16 \
  --smooth_alpha 0.50 \
  --epsilon_ratio 0.10 \
  --report_file evaluation/reports/EVALUATION_DR_REPORT.md
```

### 2. High-Throughput Clean Baseline Benchmark
```bash
python3 in_hand_manipulation/evaluate.py \
  --checkpoint models/best_model_clean.pth \
  --episodes_per_range 100 \
  --num_workers 16 \
  --epsilon_ratio 0.10
```

### 3. One-Click Suite Execution
```bash
bash scripts/run_benchmark.sh
```
