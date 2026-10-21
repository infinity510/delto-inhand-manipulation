#!/usr/bin/env bash
# High-Throughput 16-Worker Benchmark Execution Script for Delto-3F Gripper
# Runs both clean nominal baseline and stressed sim-to-real domain randomization benchmarks.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

echo "=========================================================================="
echo " Starting Full Stratified Benchmark Suite (600 Episodes / Benchmark)"
echo " Workspace: ${PROJECT_ROOT}"
echo "=========================================================================="

CHECKPOINT_DR="${PROJECT_ROOT}/models/best_model_with_dr.pth"
CHECKPOINT_CLEAN="${PROJECT_ROOT}/models/best_model_clean.pth"
REPORT_OUTPUT="${PROJECT_ROOT}/evaluation/reports/EVALUATION_DR_REPORT.md"

if [ ! -f "${CHECKPOINT_DR}" ]; then
  echo "Error: Champion model not found at ${CHECKPOINT_DR}"
  exit 1
fi

echo ""
echo "[Step 1/2] Running 16-Worker Sim-to-Real Domain Randomization Benchmark..."
python3 src/evaluation/evaluate_dr.py \
  --checkpoint "${CHECKPOINT_DR}" \
  --episodes_per_range 100 \
  --num_workers 16 \
  --smooth_alpha 0.50 \
  --epsilon_ratio 0.10 \
  --report_file "${REPORT_OUTPUT}"

echo ""
echo "[Step 2/2] Running 16-Worker Nominal Clean Baseline Benchmark..."
python3 src/evaluation/evaluate.py \
  --checkpoint "${CHECKPOINT_CLEAN}" \
  --episodes_per_range 100 \
  --num_workers 16 \
  --epsilon_ratio 0.10

echo ""
echo "=========================================================================="
echo " Benchmark Complete! Report saved to: ${REPORT_OUTPUT}"
echo "=========================================================================="
