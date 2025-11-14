from src.eval_metrics import keyword_coverage, context_overlap, retrieval_hit_at_k, citation_recall, faithfulness_stub

def test_keyword_coverage_basic():
    ans = "braf v600e is an oncogenic driver enabling targeted therapy"
    kws = ["braf v600e", "melanoma", "oncogenic driver", "targeted therapy"]
    cov = keyword_coverage(ans, kws)
    assert 0.49 < cov < 0.76  # 2/4 or 3/4 depending on exact phrasing

def test_context_overlap_basic():
    ans = "braf v600e oncogenic driver"
    ctx = "braf v600e is an oncogenic driver mutation"
    ov = context_overlap(ans, ctx)
    assert ov > 0.5

def test_hit_at_k_and_citation_recall():
    hit = retrieval_hit_at_k(["a.md", "b.md", "c.md"], {"b.md", "x.md"}, k=2)
    assert hit == 1.0
    ans = {"citations": [{"doc_id": "b.md", "quote": "x"}]}
    rec = citation_recall(ans, {"b.md", "z.md"})
    assert 0.4 < rec < 0.6

def test_faithfulness_stub():
    ans = {"claim": "oncogenic driver", "citations": [{"doc_id": "x", "quote": "driver is oncogenic"}]}
    assert faithfulness_stub(ans) == 1.0
