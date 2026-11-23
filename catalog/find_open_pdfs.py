"""Find public full-text locations for cataloged AMJ editorials via OpenAlex."""

from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
ROWS = json.loads((ROOT / "collection.json").read_text(encoding="utf-8"))


def lookup(row):
    url = "https://api.openalex.org/works/https://doi.org/" + row["doi"]
    req = urllib.request.Request(url, headers={"User-Agent": "AMJ-writing-coach-catalog/1.0 (open-access lookup)"})
    with urllib.request.urlopen(req, timeout=25) as response:
        item = json.load(response)
    return {
        "doi": row["doi"],
        "open_access": item.get("open_access"),
        "locations": [
            {"landing_page_url": x.get("landing_page_url"), "pdf_url": x.get("pdf_url"),
             "source": (x.get("source") or {}).get("display_name"), "is_oa": x.get("is_oa")}
            for x in item.get("locations", [])
        ],
    }


def main():
    output = ROOT / "openalex-locations.json"
    previous = json.loads(output.read_text(encoding="utf-8")) if output.exists() else {}
    results = {x["doi"]: x for x in previous} if isinstance(previous, list) else previous
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(lookup, row): row for row in ROWS if row["doi"] not in results}
        for future in as_completed(futures):
            row = futures[future]
            try:
                results[row["doi"]] = future.result()
                n = len(results[row["doi"]]["locations"])
                print(row["doi"], n)
            except Exception as exc:
                print(row["doi"], "ERROR", exc)
    output.write_text(json.dumps(list(results.values()), ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
