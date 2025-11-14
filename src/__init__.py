"""Clinical + Genomic RAG Evaluation Demo.

Components:
- section-aware chunking (lightweight)
- simple BM25-like retriever (pure Python)
- answer stub (templated JSON with citations)
- evaluation metrics: hit@k, citation_recall, keyword_coverage, context_overlap, faithfulness_stub
"""
