"""Render per-paper reading provenance for the public skill."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
catalog = json.loads((ROOT / "catalog" / "collection.json").read_text(encoding="utf-8"))
evidence = {x["doi"]: x for x in json.loads((ROOT / "catalog" / "reading-evidence.json").read_text(encoding="utf-8"))}
assert len(catalog) == 35 and len(evidence) == 8
assert set(evidence) <= {x["doi"] for x in catalog}

lines = [
    "# 35 篇阅读与下载状态",
    "",
    "更新于 2026-11-23。官方合集的 35 篇题录均已核对；本地取得 7 篇合集文章 PDF，另有 1 篇与原七篇系列重合的本地 PDF。已取得全文的文章有原创的重点章节阅读笔记。其余 27 篇仅完成题录收集，不能据题名推断全文观点。",
    "",
    "PDF 只在私人本地文献库；公开仓库保留来源链接、阅读依据与原创转述。公开链接的可用性可能变化。",
    "",
    "| # | 年月 | 论文 | 状态 | 全文来源 |",
    "| ---: | :--- | :--- | :--- | :--- |",
]
for row in catalog:
    item = evidence.get(row["doi"])
    state = "取得 PDF，已做重点章节笔记" if item else "待取得全文和精读"
    source = f"[{item['version']}]({item['full_text_url']})" if item else "—"
    title = row["title"].replace("|", "\\|")
    lines.append(f"| {row['number']} | {row['issue_month']} | [{title}]({row['url']}) | {state} | {source} |")
lines.extend(["", "已完成笔记见 [paper-notes.md](paper-notes.md)；合集完整题录见 [collection.md](collection.md)。", ""])
target = ROOT / "amj-editorials-coach" / "references" / "reading-status.md"
target.write_text("\n".join(lines), encoding="utf-8")
print(f"Rendered {len(catalog)} statuses: {len(evidence)} with PDFs, {len(catalog)-len(evidence)} pending")
