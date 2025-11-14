from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from .retriever import BM25Lite, Doc

@dataclass
class Retrieved:
    doc_id: str
    text: str
    score: float

class Pipeline:
    """Retrieve → create templated JSON answer with citations (stub)."""

    def __init__(self, corpus_dir: str):
        self.retriever = BM25Lite(corpus_dir)

    def retrieve(self, question: str, top_k: int = 3) -> List[Retrieved]:
        pairs: List[Tuple[Doc, float]] = self.retriever.retrieve(question, top_k=top_k)
        return [Retrieved(doc_id=d.doc_id, text=d.text, score=s) for d, s in pairs]

    def answer_stub(self, qid: str, question: str, ctxs: List[Retrieved], max_chars: int = 240) -> Dict[str, Any]:
        """Build a tiny answer JSON using the top contexts and short quotes."""
        citations = []
        claim_parts = []
        for c in ctxs[:2]:
            snippet = c.text.strip().replace("\n", " ")
            if len(snippet) > max_chars:
                snippet = snippet[:max_chars].rsplit(" ", 1)[0] + "..."
            citations.append({"doc_id": c.doc_id, "quote": snippet, "char_span": [0, min(len(snippet), max_chars)]})
            claim_parts.append(snippet.split(".")[0])
        claim = " ".join(claim_parts[:1]) or "Evidence-based summary pending."
        return {
            "question_id": qid,
            "claim": claim,
            "citations": citations,
            "guideline_refs": [],
            "confidence": 0.5
        }

    def run(self, qid: str, question: str, top_k: int = 3) -> Tuple[Dict[str, Any], List[Retrieved]]:
        ctxs = self.retrieve(question, top_k=top_k)
        ans = self.answer_stub(qid, question, ctxs)
        return ans, ctxs
