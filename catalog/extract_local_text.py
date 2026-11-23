"""Extract private study text from downloaded PDFs; keep output out of Git."""

from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "papers" / "fte" / "text"
DEST.mkdir(parents=True, exist_ok=True)

for path in sorted((ROOT / "papers" / "fte").glob("*.pdf")):
    reader = PdfReader(str(path))
    parts = []
    for number, page in enumerate(reader.pages, 1):
        parts.append(f"\n\n===== PDF page {number} =====\n\n{page.extract_text() or ''}")
    output = DEST / (path.stem + ".txt")
    output.write_text("".join(parts), encoding="utf-8")
    print(path.name, len(reader.pages), output.stat().st_size)
