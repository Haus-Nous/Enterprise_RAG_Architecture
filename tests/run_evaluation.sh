#!/bin/bash

# run_evaluation.sh
# Shell wrapper for CI/CD Pipeline to run the evaluation scripts
set -e

echo "=========================================="
echo "🚀 Starting Ask My Docs Evaluation Pipeline"
echo "=========================================="

export PYTHONPATH=$(pwd)

# Default to 1 for quick CI validation sanity checks, can be overridden via flag later
NUM_QUESTIONS=5

echo "1) Generating Golden Dataset ($NUM_QUESTIONS questions)..."
python3 tests/create_eval_dataset.py

echo "\n2) Running Ragas Evaluation..."
python3 tests/evaluate_rag.py

echo "\n✅ Evaluation Pipeline completed successfully."
echo "View detailed results in tests/eval_results.json"
echo "=========================================="
