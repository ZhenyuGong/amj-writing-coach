"""Download public repository PDFs into the ignored local papers/fte folder.

PDFs are for private study and never belong in the public Git repository.
"""

import hashlib
import json
from pathlib import Path
import subprocess

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "papers" / "fte"
DEST.mkdir(parents=True, exist_ok=True)

URLS = {
    "10.5465/amj.2026.4003": "https://spiral.imperial.ac.uk/bitstreams/ca7e1cfa-54ac-41e5-892e-bf4f387db919/download",
    "10.5465/amj.2025.4002": "https://discovery.ucl.ac.uk/10207171/1/Rouse-et-al-2025-making-a-theoretical-contribution-with-qualitative-research.pdf",
    "10.5465/amj.2024.4005": "https://discovery.ucl.ac.uk/id/eprint/10200041/1/Ravasi_dorobantu-et-al-2024-the-amj-management-research-canvas-a-tool-for-conducting-and-reporting-empirical-research.pdf",
    "10.5465/amj.2024.4003": "https://discovery.ucl.ac.uk/id/eprint/10194547/1/ravasi-et-al-2024-what-makes-research-collaborations-successful-advice-from-amj-authors.pdf",
    "10.5465/amj.2023.4006": "https://www.repository.cam.ac.uk/bitstreams/0e87c901-03ef-4031-ab08-d39c9fae33fb/download",
    "10.5465/amj.2023.4004": "https://www.repository.cam.ac.uk/bitstreams/ff41b8d0-6303-4b4f-a01d-7403ad2615b2/download",
    "10.5465/amj.2017.4003": "https://www.phdgps.com/_files/ugd/db3e44_47185a0694a04dd7a6c110b630cf9a53.pdf",
}


def main():
    rows = {r["doi"]: r for r in json.loads((ROOT / "catalog" / "collection.json").read_text(encoding="utf-8"))}
    manifest = []
    for doi, url in URLS.items():
        row = rows[doi]
        name = f"{row['issue_month']}-{doi.rsplit('.', 1)[-1]}.pdf"
        path = DEST / name
        if not path.exists():
            done = subprocess.run(["curl.exe", "-L", "--fail", "--silent", "--show-error", "--max-time", "45", url, "-o", str(path)], capture_output=True, text=True)
            if done.returncode:
                print(name, "ERROR", done.stderr.strip())
                continue
        if path.read_bytes()[:5] != b"%PDF-":
            print(name, "ERROR not a PDF")
            path.unlink()
            continue
        pages = len(PdfReader(str(path)).pages)
        manifest.append({"doi": doi, "path": str(path.relative_to(ROOT)), "source_url": url,
                         "bytes": path.stat().st_size, "pages": pages,
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        print(name, pages, path.stat().st_size)
    (DEST / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
