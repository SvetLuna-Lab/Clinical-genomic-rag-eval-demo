# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Dense retriever (embeddings) + hybrid scoring (planned)
- Stronger faithfulness checks (claim–evidence alignment) (planned)
- Guideline-aware boosts and section weighting (planned)
- Per-question HTML dashboard with filters (planned)

## [0.1.0] - 2025-11-14
### Added
- Pure-Python BM25-like retriever (`src/retriever.py`)
- Section-aware chunking (`src/chunking.py`)
- RAG answer stub with citations (`src/pipeline.py`)
- Evaluation metrics: `hit@k`, `citation_recall`, `keyword_coverage`, `context_overlap`, `faithfulness_stub` (`src/eval_metrics.py`)
- Runner with CLI and reports output (`src/run_eval.py`)
- HTML report generator (`src/report_html.py`)
- `Makefile` targets (`setup`, `test`, `eval`, `report`, `clean`) and `run.sh`
- Synthetic, de-identified corpus and `eval_questions.json`
- Tests: unit for metrics + smoke for runner
- README with structure, metrics, quick start

### Changed
- —

### Fixed
- —
