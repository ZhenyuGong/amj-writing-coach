# AMJ 论文写作与编辑社论：学生使用指南

这是两套相互独立的 Codex skill，均收录在本仓库。

| 展示名称 | 用途 | Codex 调用名 |
| --- | --- | --- |
| [AMJ Writing Coach](amj-writing-coach/SKILL.md) | 围绕 *Publishing in AMJ* 七篇社论，诊断和修改选题、设计、引言、假设、方法与结果、讨论、定性论文 | `$amj-writing-coach` |
| [AMJ Editorials Coach](amj-editorials-coach/SKILL.md) | 查阅 AMJ 官方 *From the Editors* 合集，并用已有全文阅读笔记辅助研究设计与写作判断 | `$amj-editorials-coach` |

两套 skill 不会自动混合。先选与你当前问题对应的一套；如果希望比较两套建议，可在提问中明确说出。它们提供写作诊断和修改建议，不会代替作者核对事实、方法与引用。

## 学生如何使用

**有 Codex 的同学：**在 GitHub 仓库主页选择 **Code → Download ZIP**，解压后将 `amj-writing-coach`、`amj-editorials-coach` 两个完整文件夹复制到本机 Codex 的 skills 目录（Windows 通常为 `C:\Users\你的用户名\.codex\skills\`；其他系统通常为 `~/.codex/skills/`）。开启新对话，再按需输入调用名和具体问题。

示例：

```text
$amj-writing-coach 请根据我下面的引言，指出研究问题和理论贡献之间最弱的一环，并给出修改稿。不要编造结果或引用。
```

```text
$amj-editorials-coach 我正在设计一项现象驱动的定量研究。请根据已精读的 AMJ 社论，比较可能的理论贡献路径，并标明建议所依据的 DOI。
```

**暂时不用 Codex 的同学：**可直接在网页阅读[七篇系列来源](amj-writing-coach/references/sources.md)、[官方合集 35 篇目录](amj-editorials-coach/references/collection.md)、[逐篇阅读状态](amj-editorials-coach/references/reading-status.md)和[已完成的阅读笔记](amj-editorials-coach/references/paper-notes.md)。

## 文献范围与使用边界

七篇写作系列已有独立的[写作指南](amj-writing-coach/references/series-guide.md)。官方 *From the Editors* 合集按 2026-11-23 页面收录 35 篇；目前其中 8 篇有本地 PDF 与重点章节笔记（包括与七篇系列重合的 1 篇），另外 27 篇已编目但尚未取得可用全文。第二套 skill 只会把已有全文和笔记的文章用于具体建议，不会根据题名猜测未读文章的观点。

仓库公开的是原创整理、题录和来源链接；论文 PDF 不随仓库分发。论文观点请以[AMJ 官方合集](https://journals.aom.org/journal/amj/fte-collection)及原文为准。本项目与 Academy of Management 无隶属关系。


