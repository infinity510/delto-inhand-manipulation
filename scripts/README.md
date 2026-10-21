# Execution & Automation Scripts (`scripts/`)

This directory provides utility launcher scripts, automated benchmark runners, and publication documentation compilers for the Delto-3F manipulation workspace.

---

## Script Inventory

| Script | Type | Description |
| :--- | :---: | :--- |
| [`run_eval_demo.sh`](run_eval_demo.sh) | Bash | Interactive, menu-driven CLI launcher for 3D visual demos, parallel benchmarks, and PDF compilation. |
| [`run_benchmark.sh`](run_benchmark.sh) | Bash | Automated 16-worker batch runner executing both clean and Sim-to-Real DR 600-episode benchmark suites. |
| [`generate_documentation_pdf.py`](generate_documentation_pdf.py) | Python | Compiles the publication-grade 55-page PDF from `docs/learning.md` with KaTeX math and Pygments code highlighting. |

---

## Usage Guide

### 1. Interactive Demo & Evaluation Launcher
```bash
bash scripts/run_eval_demo.sh
```
Interactive options:
- `1`: Run nominal clean baseline in MuJoCo 3D viewer (`models/best_model_clean.pth`).
- `2`: Run Sim-to-Real Domain Randomization champion with real-time HUD (`models/best_model_with_dr.pth`).
- `3`: Run 16-worker parallel DR benchmark (600 episodes) and save report to `evaluation/reports/EVALUATION_DR_REPORT.md`.
- `4`: Re-compile `docs/IN_HAND_MANIPULATION_DOCUMENTATION.pdf`.

Direct shortcut execution:
```bash
bash scripts/run_eval_demo.sh 1   # Launch clean viewer
bash scripts/run_eval_demo.sh 2   # Launch DR viewer
bash scripts/run_eval_demo.sh 3   # Run 16-worker benchmark
bash scripts/run_eval_demo.sh 4   # Compile documentation PDF
```

### 2. Full Benchmark Runner
```bash
bash scripts/run_benchmark.sh
```

### 3. PDF Generator
```bash
python3 scripts/generate_documentation_pdf.py
```
Outputs: `docs/IN_HAND_MANIPULATION_DOCUMENTATION.pdf`.
