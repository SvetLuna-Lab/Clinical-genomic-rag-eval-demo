# src/run_eval.py
import argparse
import csv
import json
import os
from typing import Any, Dict, List, Set

from .pipeline import Pipeline
from .eval_metrics import (
    retrieval_hit_at_k,
    citation_recall,
    keyword_coverage,
    context_overlap,
    faithfulness_stub,
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CORPUS_DIR = os.path.join(DATA_DIR, "corpus")
QUESTIONS_PATH = os.path.join(DATA_DIR, "eval_questions.json")


def load_questions(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def concat_citations_text(answer_json: dict) -> str:
    """Join citation quotes into one text for overlap checks."""
    return " ".join(c.get("quote", "") for c in answer_json.get("citations", []))


def main(
    out_jsonl: str | None = None,
    out_csv: str | None = None,
    top_k: int = 3,
    out_dir: str | None = None,
) -> None:
    """Run evaluation and write artifacts."""
    # Default to *current working directory* if out_dir is not provided.
    # This makes tests that chdir() into a tmp folder succeed.
    out_dir = out_dir or os.getcwd()
    os.makedirs(out_dir, exist_ok=True)

    out_jsonl = out_jsonl or "eval_report.jsonl"
    out_csv = out_csv or "eval_report.csv"

    out_jsonl_path = os.path.join(out_dir, out_jsonl)
    out_csv_path = os.path.join(out_dir, out_csv)

    questions = load_questions(QUESTIONS_PATH)
    pipe = Pipeline(corpus_dir=CORPUS_DIR)

    rows_csv: List[Dict[str, Any]] = []

    with open(out_jsonl_path, "w", encoding="utf-8") as jf:
        for q in questions:
            qid = q["id"]
            question = q["question"]
            expected = q.get("expected_keywords", [])
            gold_ids: Set[str] = set(q.get("must_be_grounded_in", []))

            answer_json, ctxs = pipe.run(qid, question, top_k=top_k)
            retrieved_ids = [c.doc_id for c in ctxs]

            # metrics
            hitk = retrieval_hit_at_k(retrieved_ids, gold_ids, k=top_k)
            citrec = citation_recall(answer_json, gold_ids)
            cov = keyword_coverage(answer_json.get("claim", ""), expected)
            ctx_text = concat_citations_text(answer_json)
            ovlp = context_overlap(answer_json.get("claim", ""), ctx_text)
            faith = faithfulness_stub(answer_json)

            record = {
                "id": qid,
                "question": question,
                "answer": answer_json,
                "retrieved_doc_ids": retrieved_ids,
                "metrics": {
                    "hit@k": hitk,
                    "citation_recall": citrec,
                    "keyword_coverage": cov,
                    "context_overlap": ovlp,
                    "faithfulness_stub": faith,
                },
            }
            jf.write(json.dumps(record, ensure_ascii=False) + "\n")

            rows_csv.append(
                {
                    "id": qid,
                    "hit@k": hitk,
                    "citation_recall": citrec,
                    "keyword_coverage": cov,
                    "context_overlap": ovlp,
                    "faithfulness_stub": faith,
                }
            )

    # CSV summary (per question)
    with open(out_csv_path, "w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=list(rows_csv[0].keys()))
        writer.writeheader()
        writer.writerows(rows_csv)

    print("=== Clinical+Genomic RAG evaluation complete ===")
    print(f"JSONL: {out_jsonl_path}")
    print(f"CSV:   {out_csv_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir", type=str, default=None, help="Output directory (default: CWD).")
    parser.add_argument("--out_jsonl", type=str, default=None, help="Output JSONL filename (default: eval_report.jsonl).")
    parser.add_argument("--out_csv", type=str, default=None, help="Output CSV filename (default: eval_report.csv).")
    parser.add_argument("--top_k", type=int, default=3, help="Top-k documents to retrieve.")
    args = parser.parse_args()

    main(out_jsonl=args.out_jsonl, out_csv=args.out_csv, top_k=args.top_k, out_dir=args.out_dir)
