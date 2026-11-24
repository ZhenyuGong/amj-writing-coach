# AMJ Writing Coach

Skill display names: **AMJ Writing Coach** and **AMJ Editorials Coach**. Codex invocation IDs remain lowercase (`$amj-writing-coach`, `$amj-editorials-coach`) as required by its skill name format.

[中文使用与分享指南](README.zh-CN.md)

A Codex skill based on the seven-part *Publishing in AMJ* editorial series (2011–2012). It helps diagnose, plan, draft, and revise empirical management papers. The skill contains original synthesis and links to the source articles.

The repository also contains a separate skill for AMJ's broader *From the Editors* collection. The original seven-part writing coach remains independent. See the [35-item collection inventory](amj-editorials-coach/references/collection.md), [reading status for every item](amj-editorials-coach/references/reading-status.md), [substantive notes for the accessible papers](amj-editorials-coach/references/paper-notes.md), [CSV](catalog/collection.csv), and [JSON](catalog/collection.json).

As of 2026-11-23, eight collection articles have a local PDF and reading notes, including one that overlaps the seven-part series. The other 27 are cataloged but await accessible full text. The broader skill uses only the read subset for article-specific advice. It does not encode the repository owner's personal writing style.

## Install

Copy either skill folder into your Codex skills directory, typically `~/.codex/skills/`, and start a new chat. Invoke `$amj-writing-coach` for the seven-part writing series or `$amj-editorials-coach` for the broader editorial collection.

## Sources and rights

See [the source index](amj-writing-coach/references/sources.md) for the original seven DOIs. The PDFs are kept locally in `papers/` for private study and excluded from Git. This repository does not redistribute the articles or claim affiliation with the Academy of Management.
