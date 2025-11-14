# Clinical-genomic-rag-eval-demo
[![CI](https://github.com/SvetLuna-Lab/clinical-genomic-rag-eval-demo/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/SvetLuna-Lab/clinical-genomic-rag-eval-demo/actions/workflows/ci.yml)


Clinical + Genomic **RAG evaluation** on de-identified synthetic data with transparent grounding and reproducible metrics.  
Python **3.10+**. No runtime deps beyond the standard library (tests use `pytest`).

---

## Why
Clinical answers must be **grounded** and **auditable**. This demo:
- enforces **citations** (doc_id + quote spans),
- measures **retrieval quality** and **faithfulness**,
- produces **JSONL / CSV / HTML** reports in `reports/`,
- is small, fast, and easy to extend with dense retrievers and real LLMs.

---

## Repository structure

```text
clinical-genomic-rag-eval-demo/
├─ .github/
│  └─ workflows/
│     └─ ci.yml                  # GitHub Actions: tests + smoke eval + artifacts
├─ data/
│  ├─ corpus/
│  │  ├─ clin_note_001.md        # synthetic clinical note (de-identified)
│  │  ├─ genomics_oncokb_excerpt.md  # synthetic genomic knowledge snippet
│  │  ├─ pubmed_abstract_001.md  # synthetic pubmed-like abstract
│  │  └─ schema_examples/
│  │     ├─ answer_template.json # answer JSON schema (template)
│  │     └─ doc_schema.md        # corpus/chunking guidance
│  └─ eval_questions.json        # questions + gold grounding + keywords
├─ reports/
│  └─ .gitkeep                   # keep folder in VCS (artifacts land here)
├─ src/
│  ├─ __init__.py
│  ├─ chunking.py                # section-aware chunking (HPI / A&P / Pathology)
│  ├─ retriever.py               # pure-Python BM25-like retriever
│  ├─ pipeline.py                # retrieve → answer stub (citations)
│  ├─ eval_metrics.py            # hit@k, citation_recall, keyword_coverage, ...
│  ├─ run_eval.py                # run evaluation → JSONL/CSV in reports/
│  └─ report_html.py             # JSONL → HTML summary report
├─ tests/
│  ├─ test_metrics.py            # unit tests for metrics
│  └─ test_pipeline_smoke.py     # smoke: run_eval produces artifacts
├─ .editorconfig
├─ .gitattributes
├─ .gitignore
├─ .pre-commit-config.yaml       # optional local checks (black/ruff/hooks)
├─ CHANGELOG.md
├─ Makefile                      # setup / test / eval / report / clean
├─ requirements.txt              # pytest + pytest-cov (tests only)
├─ requirements-dev.txt          # optional dev tools (black/ruff/pre-commit)
└─ run.sh                        # orchestrate eval + HTML report



Metrics

hit@k — is any gold doc_id in the top-k retrieved?

citation_recall — fraction of gold docs cited in the answer.

keyword_coverage — expected keywords present in the claim (substring, case-insensitive).

context_overlap — token overlap of claim vs concatenated citation quotes (sanity for grounding).

faithfulness_stub — every citation quote shares words with the claim (very rough check).

All metrics are computed per-question and written to reports/eval_report.csv and reports/eval_report.jsonl.


Quick start

Python 3.10+

# 1) Install test deps
pip install -r requirements.txt

# 2) Run tests
pytest -q

# 3) Run evaluation (artifacts → reports/)
python -m src.run_eval --out_dir reports --top_k 3

# 4) Build HTML summary from JSONL
python -m src.report_html --in_jsonl reports/eval_report.jsonl --out_html reports/report.html



Makefile shortcuts

make setup     # pip install -r requirements.txt
make test      # pytest
make eval      # run_eval → JSONL/CSV in reports/
make report    # report_html → reports/report.html
make clean     # remove artifacts


One-liner

./run.sh 3
# JSONL → reports/eval_report.jsonl
# CSV   → reports/eval_report.csv
# HTML  → reports/report.html


Console output example

=== Clinical+Genomic RAG evaluation complete ===
JSONL: /.../reports/eval_report.jsonl
CSV:   /.../reports/eval_report.csv
HTML saved: /.../reports/report.html



Data & safety

Corpus is synthetic and de-identified (for demo only).

Section markers in clinical notes: ## HPI, ## Assessment and Plan, ## Pathology.

See data/corpus/schema_examples/doc_schema.md for formatting guidance.


Extending

Swap BM25-lite for a dense retriever (embeddings) and/or hybrid scoring.

Replace answer_stub with a real LLM client; keep the output JSON schema.

Strengthen faithfulness: claim–evidence alignment checks, factual consistency.

Add guideline-aware boosts (e.g., NCCN/ESMO) and section weighting.

Promote CI to publish report.html as a build artifact or Pages.


## Versioning

We follow Semantic Versioning. See [CHANGELOG.md](./CHANGELOG.md).  
Initial release: **v0.1.0**.


License

If you intend to open-source, add a LICENSE (e.g., MIT).
Synthetic content provided here is for demonstration and carries no clinical guarantees.


Acknowledgements

This repository was designed to help teams prototype grounded clinical RAG with auditable, lightweight metrics before integrating production corpora and models.


