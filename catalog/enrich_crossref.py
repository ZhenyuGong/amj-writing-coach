"""Enrich a manually checked AMJ collection list with Crossref metadata.

The official collection page, not Crossref search, determines membership.
Crossref is used only to identify likely DOIs and bibliographic metadata.
Review every low-score or missing match before publishing the result.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
SEEDS = json.loads((ROOT / "collection-seed.json").read_text(encoding="utf-8"))
KNOWN_DOIS = {
    "2026-04": "10.5465/amj.2026.4002",
    "2025-12": "10.5465/amj.2025.4006",
    "2024-12": "10.5465/amj.2024.4006",
    "2024-06": "10.5465/amj.2024.4003",
    "2024-02": "10.5465/amj.2024.4001",
    "2021-08": "10.5465/amj.2021.4004",
    "2019-06": "10.5465/amj.2019.4003",
}


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower().replace("’", "'")).strip()


def lookup(item):
    query = urllib.parse.urlencode({"query.title": item["title"], "rows": 5})
    url = f"https://api.crossref.org/works?{query}"
    req = urllib.request.Request(url, headers={"User-Agent": "AMJ-writing-coach-catalog/1.0 (bibliographic lookup)"})
    with urllib.request.urlopen(req, timeout=25) as response:
        works = json.load(response)["message"]["items"]
    choices = []
    for work in works:
        title = (work.get("title") or [""])[0]
        journal = (work.get("container-title") or [""])[0]
        score = SequenceMatcher(None, norm(item["title"]), norm(title)).ratio()
        if "academy of management journal" in journal.lower():
            score += 0.08
        if work.get("published", {}).get("date-parts", [[None]])[0][0] == int(item["date"][:4]):
            score += 0.03
        choices.append((score, work))
    score, work = max(choices, key=lambda pair: pair[0])
    result = dict(item)
    result.update({
        "matched_title": (work.get("title") or [""])[0],
        "authors": "; ".join(" ".join(filter(None, (a.get("given"), a.get("family")))) for a in work.get("author", [])),
        "doi": work.get("DOI", ""),
        "journal": (work.get("container-title") or [""])[0],
        "volume": work.get("volume", ""),
        "issue": work.get("issue", ""),
        "pages": work.get("page", ""),
        "match_score": round(score, 3),
    })
    return result


def lookup_doi(item):
    doi = KNOWN_DOIS[item["date"]]
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='/')}"
    req = urllib.request.Request(url, headers={"User-Agent": "AMJ-writing-coach-catalog/1.0 (bibliographic lookup)"})
    with urllib.request.urlopen(req, timeout=25) as response:
        work = json.load(response)["message"]
    result = dict(item)
    result.update({
        "matched_title": (work.get("title") or [""])[0],
        "authors": "; ".join(" ".join(filter(None, (a.get("given"), a.get("family")))) for a in work.get("author", [])),
        "doi": work.get("DOI", ""),
        "journal": (work.get("container-title") or [""])[0],
        "volume": work.get("volume", ""),
        "issue": work.get("issue", ""),
        "pages": work.get("page", ""),
        "match_score": round(SequenceMatcher(None, norm(item["title"]), norm((work.get("title") or [""])[0])).ratio(), 3),
    })
    return result


def main():
    output = ROOT / "crossref-candidates.json"
    results = json.loads(output.read_text(encoding="utf-8")) if output.exists() else [None] * len(SEEDS)
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {pool.submit(lookup_doi if item["date"] in KNOWN_DOIS else lookup, item): i
                   for i, item in enumerate(SEEDS) if not results[i] or "error" in results[i]}
        for future in as_completed(futures):
            i = futures[future]
            try:
                results[i] = future.result()
            except Exception as exc:
                results[i] = dict(SEEDS[i], error=str(exc))
            print(f"{i+1:02d} {results[i].get('match_score', 'ERR')} {results[i].get('doi', '')} {SEEDS[i]['title'][:65]}")
    output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
