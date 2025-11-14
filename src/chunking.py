from dataclasses import dataclass
from typing import List, Tuple

SECTION_HEADERS = ("## HPI", "## Assessment and Plan", "## Pathology")

@dataclass
class Chunk:
    doc_id: str
    text: str
    section: str
    span: Tuple[int, int]  # char offsets in original doc

def section_aware_chunks(doc_id: str, text: str, max_len: int = 1000) -> List[Chunk]:
    """Very simple section-aware chunking: split by known headers, then slice."""
    chunks: List[Chunk] = []
    pos = 0
    lines = text.splitlines()
    current_section = "BODY"
    buffer = []
    start_pos = 0

    def flush(section: str, buf: List[str], start: int, end: int) -> None:
        s = "\n".join(buf).strip()
        if not s:
            return
        # slice long blobs into smaller pieces
        i = 0
        while i < len(s):
            j = min(i + max_len, len(s))
            chunks.append(Chunk(doc_id=doc_id, text=s[i:j], section=section, span=(start + i, start + j)))
            i = j

    for line in lines:
        line_with_nl = line + "\n"
        if any(line.startswith(h) for h in SECTION_HEADERS):
            flush(current_section, buffer, start_pos, pos)
            current_section = line.strip().lstrip("# ").strip()
            buffer = [line]
            start_pos = pos
        else:
            buffer.append(line)
        pos += len(line_with_nl)

    flush(current_section, buffer, start_pos, pos)
    return chunks
