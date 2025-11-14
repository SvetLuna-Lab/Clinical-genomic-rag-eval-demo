from typing import Any, List, Sequence, Set

def _tok(t: str) -> List[str]:
    toks = []
    for raw in t.lower().split():
        tok = "".join(ch for ch in raw if ch.isalnum())
        if tok:
            toks.append(tok)
    return toks

def retrieval_hit_at_k(retrieved_doc_ids: Sequence[str], gold_doc_ids: Set[str], k: int = 3) -> float:
    """1.0 if any gold doc appears in top-k retrieved; else 0.0."""
    top = retrieved_doc_ids[:k]
    return 1.0 if any(d in gold_doc_ids for d in top) else 0.0

def citation_recall(answer_json: dict, gold_doc_ids: Set[str]) -> float:
    """Recall over gold docs present in the answer citations."""
    if not gold_doc_ids:
        return 0.0
    cited = {c.get("doc_id", "") for c in answer_json.get("citations", [])}
    hits = len(gold_doc_ids.intersection(cited))
    return hits / len(gold_doc_ids)

def keyword_coverage(answer_text: str, expected_keywords: Sequence[str]) -> float:
    """Fraction of expected keywords present (substring match, case-insensitive)."""
    if not expected_keywords:
        return 0.0
    a = answer_text.lower()
    hits = sum(1 for kw in expected_keywords if kw.lower() in a)
    return hits / len(expected_keywords)

def context_overlap(answer_text: str, citations_text: str) -> float:
    """Token-level overlap: fraction of answer tokens found in concatenated citations text."""
    a_toks = _tok(answer_text)
    c_set = set(_tok(citations_text))
    return 0.0 if not a_toks else sum(1 for t in a_toks if t in c_set) / len(a_toks)

def faithfulness_stub(answer_json: dict) -> float:
    """1.0 if each citation 'quote' actually contains words from the 'claim' (very rough check)."""
    claim_toks = set(_tok(answer_json.get("claim", "")))
    if not claim_toks:
        return 0.0
    cites = answer_json.get("citations", [])
    if not cites:
        return 0.0
    for c in cites:
        q_toks = set(_tok(c.get("quote", "")))
        if not claim_toks.intersection(q_toks):
            return 0.0
    return 1.0
