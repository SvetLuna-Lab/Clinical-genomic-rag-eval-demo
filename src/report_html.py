import argparse
import html
import json
import os
from typing import Any, Dict, List


def load_jsonl(path: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def escape(s: str) -> str:
    return html.escape(s, quote=True)


def build_html(rows: List[Dict[str, Any]]) -> str:
    # aggregate metrics
    def avg(key: str) -> float:
        vals = [r["metrics"].get(key, 0.0) for r in rows if "metrics" in r]
        return sum(vals) / len(vals) if vals else 0.0

    agg = {
        "hit@k": avg("hit@k"),
        "citation_recall": avg("citation_recall"),
        "keyword_coverage": avg("keyword_coverage"),
        "context_overlap": avg("context_overlap"),
        "faithfulness_stub": avg("faithfulness_stub"),
    }

    head = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Clinical+Genomic RAG — Evaluation Report</title>
<style>
 body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Arial,sans-serif;margin:24px;color:#111}
 h1{margin:0 0 8px 0}
 .meta{color:#555;margin-bottom:16px}
 table{border-collapse:collapse;width:100%;margin:16px 0}
 th,td{border:1px solid #ddd;padding:8px;vertical-align:top}
 th{background:#f6f6f6;text-align:left}
 code{background:#f2f2f2;padding:2px 4px;border-radius:4px}
 .badge{display:inline-block;padding:2px 6px;border-radius:6px;background:#eef;border:1px solid #99c;color:#224;margin-right:6px}
 .section{margin-top:24px}
 .small{color:#666;font-size:12px}
</style>
</head>
<body>
"""

    summary = f"""
<h1>Clinical+Genomic RAG — Evaluation Report</h1>
<div class="meta">Simple metrics over synthetic, de-identified corpus.</div>
<div class="section">
  <div class="badge">hit@k: {agg['hit@k']:.3f}</div>
  <div class="badge">citation_recall: {agg['citation_recall']:.3f}</div>
  <div class="badge">keyword_coverage: {agg['keyword_coverage']:.3f}</div>
  <div class="badge">context_overlap: {agg['context_overlap']:.3f}</div>
  <div class="badge">faithfulness_stub: {agg['faithfulness_stub']:.3f}</div>
</div>
"""

    # per-question table
    rows_html = []
    for r in rows:
        qid = escape(str(r.get("id", "")))
        q = escape(r.get("question", ""))
        mets = r.get("metrics", {})
        mline = " | ".join(
            f"{escape(k)}={float(v):.3f}" for k, v in mets.items()
        )
        # citations
        ans = r.get("answer", {})
        cites = ans.get("citations", [])
        cite_html = "<ul>" + "".join(
            f"<li><b>{escape(c.get('doc_id',''))}</b>: {escape(c.get('quote',''))}</li>"
            for c in cites
        ) + "</ul>"
        rows_html.append(
            f"<tr><td><b>{qid}</b></td><td>{q}</td><td>{mline}</td><td>{cite_html}</td></tr>"
        )

    table = f"""
<div class="section">
  <table>
    <thead>
      <tr>
        <th>Question ID</th>
        <th>Question</th>
        <th>Metrics</th>
        <th>Citations</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows_html)}
    </tbody>
  </table>
  <div class="small">Note: faithfulness_stub is a rough heuristic. Replace with stronger checks later.</div>
</div>
"""

    foot = """
</body>
</html>"""
    return head + summary + table + foot


def main(in_jsonl: str, out_html: str) -> None:
    data = load_jsonl(in_jsonl)
    html_doc = build_html(data)
    os.makedirs(os.path.dirname(out_html) or ".", exist_ok=True)
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_doc)
    print(f"HTML saved: {out_html}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--in_jsonl", required=True, help="Path to eval_report.jsonl")
    p.add_argument("--out_html", required=True, help="Path to output HTML")
    args = p.parse_args()
    main(args.in_jsonl, args.out_html)
