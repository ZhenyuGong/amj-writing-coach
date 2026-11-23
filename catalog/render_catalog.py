"""Render the verified AMJ From the Editors inventory from Crossref candidates."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
TOPICS = [
    "审稿", "研究方法文章", "现象驱动研究", "AI与研究责任", "编辑方针",
    "编辑方针", "专题论坛", "定量研究", "理论与经典", "定性研究",
    "期刊运作", "跨学科理论", "研究设计与写作", "理论—方法—数据", "科研合作",
    "新数据来源", "研究方法文章", "生成式AI", "新现象与理论定位", "混合方法",
    "方法创新", "AI研究机会", "编辑方针", "研究透明度", "投稿与原创性",
    "实践价值与责任", "研究重要性", "跨学科写作", "实践影响", "理论起点",
    "数据重复使用", "引言写作", "定性方法", "研究情境与样本", "定性写作与审稿",
]


def main():
    candidates = json.loads((ROOT / "crossref-candidates.json").read_text(encoding="utf-8"))
    assert len(candidates) == len(TOPICS) == 35
    assert len({item["doi"].lower() for item in candidates}) == 35
    assert all("academy of management journal" in item["journal"].lower() for item in candidates)
    assert all(item["match_score"] >= 0.8 for item in candidates)

    rows = []
    for n, (item, topic) in enumerate(zip(candidates, TOPICS), 1):
        rows.append({
            "number": n,
            "issue_month": item["date"],
            "title": item["title"],
            "authors": item["authors"],
            "journal": "Academy of Management Journal",
            "volume": item["volume"],
            "issue": item["issue"],
            "pages": item["pages"],
            "doi": item["doi"].lower(),
            "url": f"https://doi.org/{item['doi'].lower()}",
            "topic": topic,
            "also_in_2011_2012_seven_part_series": item["doi"].lower() == "10.5465/amj.2011.4000",
        })

    (ROOT / "collection.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (ROOT / "collection.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# AMJ From the Editors 官方合集目录",
        "",
        "来源：[Academy of Management Journal 官方合集](https://journals.aom.org/journal/amj/fte-collection)。按该页面 2026-11-23 的展示顺序收录，共 **35 篇**。这是官方精选页面的目录，不等于 AMJ 历年所有 From the Editors 文章。题名与成员资格据官方合集页面；DOI、作者及卷期页码用 Crossref 元数据核对。页面以后可能更新。",
        "",
        "这是文献目录。逐篇阅读状态与已完成的原创笔记见 [阅读记录](reading-status.md) 和 [精读笔记](paper-notes.md)。主题栏是本仓库按题名制作的检索标签，不代表期刊正式分类。完整作者和机器可读元数据见仓库中的 [CSV](https://github.com/ZhenyuGong/amj-writing-coach/blob/main/catalog/collection.csv) 与 [JSON](https://github.com/ZhenyuGong/amj-writing-coach/blob/main/catalog/collection.json)。",
        "",
        "原有的 2011–2012 年七篇 `Publishing in AMJ` 系列与此精选页面并不等同：本页面只列出系列第 3 篇 *Setting the Hook*。原七篇仍见 [七篇系列索引](../../amj-writing-coach/references/sources.md)。",
        "",
        "| # | 期次 | 文章（DOI 链接） | 主题 |",
        "| ---: | :--- | :--- | :--- |",
    ]
    for row in rows:
        title = row["title"].replace("|", "\\|")
        lines.append(f"| {row['number']} | {row['issue_month']} | [{title}]({row['url']}) | {row['topic']} |")
    lines += [
        "",
        "## 使用边界",
        "",
        "- 35 篇均已编目并核对 DOI；只有在 [阅读记录](reading-status.md) 标为已有全文与实质阅读笔记的文章可作为提炼建议的依据。",
        "- 公开 GitHub 仓库仅保存目录、原创总结和链接，不存放受版权保护的论文 PDF。",
        "",
    ]
    (PROJECT / "amj-fte-research-coach" / "references" / "collection.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Rendered {len(rows)} collection entries")


if __name__ == "__main__":
    main()
