# Minimal makefile for clinical-genomic-rag-eval-demo

PY=python
PKG=src

.PHONY: help setup test eval report clean

help:
	@echo "Targets:"
	@echo "  setup   - install test deps (pytest, pytest-cov)"
	@echo "  test    - run unit tests"
	@echo "  eval    - run evaluation → reports/eval_report.jsonl + .csv"
	@echo "  report  - build HTML report from JSONL → reports/report.html"
	@echo "  clean   - remove reports/* and __pycache__"

setup:
	$(PY) -m pip install -r requirements.txt

test:
	$(PY) -m pytest -q

eval:
	$(PY) -m $(PKG).run_eval --out_dir reports --top_k 3

report:
	$(PY) -m $(PKG).report_html --in_jsonl reports/eval_report.jsonl --out_html reports/report.html

clean:
	@rm -f reports/*.jsonl reports/*.csv reports/*.html || true
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
