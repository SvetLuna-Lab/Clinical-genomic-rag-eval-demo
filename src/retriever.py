import math
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class Doc:
    doc_id: str
    text: str

class BM25Lite:
    """Pure-Python, minimal BM25-like retriever (sufficient for demo)."""

    def __init__(self, corpus_dir: str, k1: float = 1.5, b: float = 0.75):
        self.corpus_dir = corpus_dir
        self.k1, self.b = k1, b
        self.docs: List[Doc] = []
        self.doc_len: Dict[str, int] = {}
        self.df: Dict[str, int] = {}
        self.N = 0
        self.avg_len = 0.0
        self._load()
        self._index()

    @staticmethod
    def _tok(t: str) -> List[str]:
        toks = []
        for raw in t.lower().split():
            tok = "".join(ch for ch in raw if ch.isalnum())
            if tok:
                toks.append(tok)
        return toks

    def _load(self) -> None:
        for fn in os.listdir(self.corpus_dir):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(self.corpus_dir, fn)
            with open(p, "r", encoding="utf-8") as f:
                self.docs.append(Doc(doc_id=fn, text=f.read()))
        self.N = len(self.docs)

    def _index(self) -> None:
        total = 0
        self.df.clear()
        self.doc_len.clear()
        for d in self.docs:
            toks = self._tok(d.text)
            total += len(toks)
            self.doc_len[d.doc_id] = len(toks)
            for term in set(toks):
                self.df[term] = self.df.get(term, 0) + 1
        self.avg_len = total / self.N if self.N else 0.0

    def _score(self, q_toks: List[str], d: Doc) -> float:
        if self.N == 0:
            return 0.0
        dtoks = self._tok(d.text)
        if not dtoks:
            return 0.0
        tf: Dict[str, int] = {}
        for t in dtoks:
            tf[t] = tf.get(t, 0) + 1
        score = 0.0
        L = len(dtoks)
        for term in q_toks:
            if term not in tf:
                continue
            df = self.df.get(term, 0)
            if df == 0:
                continue
            idf = math.log((self.N - df + 0.5) / (df + 0.5) + 1.0)
            freq = tf[term]
            denom = freq + self.k1 * (1 - self.b + self.b * L / (self.avg_len or 1.0))
            score += idf * (freq * (self.k1 + 1) / denom)
        return score

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[Doc, float]]:
        q = self._tok(query)
        scored = [(d, self._score(q, d)) for d in self.docs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
