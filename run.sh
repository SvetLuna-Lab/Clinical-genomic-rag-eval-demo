#!/usr/bin/env bash
set -euo pipefail

# Orchestrate evaluation + HTML report
# Usage: ./run.sh [TOP_K]
TOP_K="${1:-3}"

mkdir -p reports

python -m src.run_eval --out_dir reports --top_k "${TOP_K}"
python -m src.report_html --in_jsonl reports/eval_report.jsonl --out_html reports/report.html

echo "Done."
echo "JSONL  → reports/eval_report.jsonl"
echo "CSV    → reports/eval_report.csv"
echo "HTML   → reports/report.html"
