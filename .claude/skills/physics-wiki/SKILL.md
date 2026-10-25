---
name: physics-wiki
description: Navigate and maintain the physics study wiki (wiki/ in this project) built from the scanned Кучерук textbook. Use for any question about a physics topic, term, formula, textbook page or syllabus question here; for adding or changing topic pages, glossary entries or source maps; for "where is X in the book"; and for wiki health checks (lint). Covers page lookup (printed page to OCR file and scan image), search, and the ingest, query and lint workflows.
---

# Physics wiki

The wiki follows Karpathy's LLM-wiki pattern: **raw sources** (immutable) → **wiki** (Claude maintains it) → **schema** (`CLAUDE.md`). The user writes the lecture notes **by hand**. Wiki pages are scaffolds and references, never finished notes.

## Map

| Layer | Path | Rule |
|---|---|---|
| raw | `Books/raw/kucheruk{1,2,3}.pdf`, `Assignments/Lecture notest/*` | never edit |
| raw (derived) | `Books/text/kucheruk{1,2,3}/NNN{L,R}.txt` (OCR) | regenerate only via OCR on orca |
| wiki | `wiki/index.md` | **read first**; the catalog of every page |
| | `wiki/log.md` | append-only history |
| | `wiki/syllabi/*.md` | assignment question → topic page, with status |
| | `wiki/topics/<syllabus>/NN_*.md` | one page per syllabus question (scaffold for a handwritten page); folders `electrostatics/`, `molecular/` |
| | `wiki/concepts/*.md` | ideas that cut across topics |
| | `wiki/sources/kucheruk{1,2,3}.md` | chapter/§ → printed pages → spreads → topics |
| | `wiki/glossary.md` | exact Ukrainian terms, formula, EN, page |
| schema | `CLAUDE.md` | conventions, scope, backlog |

## Lookup tools (`.claude/skills/physics-wiki/scripts/`)

- `page.sh <vol> <printed page>` prints the OCR file for that page. Add `render` (with `OUT=<scratchpad>`) to get a 150 dpi PNG of the scan, then view it with Read.
  - Mapping, the same in every volume: spread N = ⌊p/2⌋ + 1, even page = L, odd page = R.
- `find.sh <term> [vol]` lists wiki pages that mention the term, then textbook hits as `т.V p.P: line`.
- To find which § covers a topic, use the § tables in `wiki/sources/kucheruk{1,2}.md` rather than grepping.

## Workflows

### Query ("what does the book say about X", "where is X")
1. Read `wiki/index.md` and go to the relevant topic, concept or source page.
2. If the wiki doesn't cover it, run `find.sh`, then read the OCR page.
3. When quoting a formula or the exact wording of a definition, **check the scan** (`page.sh … render`). The OCR garbles formulas, drop caps and exponents.
4. Answer with page refs (`т. 2, с. 38`). If the answer is worth keeping, file it into the wiki: a topic section, a concept page or a glossary entry. Then add a log line.

### Ingest (a new topic, syllabus or source)
1. Find the pages using the source map, and read the OCR for the whole §.
2. Write or extend `wiki/topics/<syllabus>/NN_*.md` using the **topic template** below.
3. Add the terms to `wiki/glossary.md` under that topic: the book's exact wording, formula, unit, EN, page.
4. Update the syllabus status, `wiki/index.md` (one line per page) and `wiki/sources/*` if new pages were mapped.
5. If an idea links several topics, create or extend a `wiki/concepts/` page.
6. Append to `wiki/log.md`: `## [YYYY-MM-DD] topic | NN Name`, plus bullets.
7. Offer to run the `glossary-validator` agent on the new entries.

### Lint (when asked, or after big changes)
Check for:
- broken relative links;
- topics missing from the index or syllabus;
- glossary terms with no page ref;
- pages with `formulas_checked: false` (list them);
- duplicated definitions between topics (each concept should be defined once and linked elsewhere);
- syllabus questions with no page;
- orphan pages.

Report the findings and fix the mechanical ones. Log the run as `lint`.

A link check: `grep -oE '\]\([^)]+\.md\)' -r wiki | …` then resolve each path relative to its file.

## Topic page template
```
---
type: topic
syllabus: <electrostatics|mkr2-molecular|…>
topic: "NN"
source: "т. V, § x.y"
status: skeleton | verified
formulas_checked: false
updated: YYYY-MM-DD
---
# NN. <syllabus wording> — каркас

[← prev](…) · [index](../../index.md) · [syllabus](../../syllabi/….md) · [glossary](../../glossary.md) · [next →](…)

📖 т. V, **§ x.y** (с. a–b). ⚠️/✅ formula check status.

## Layout       ← ASCII box plan of one handwritten page
## [A] … [F]    ← one box each: the book's exact term or definition in «», formula with eq. number, page
## Self-check   ← 2–4 questions
```
Style:
- Use the textbook's terms exactly, with the eq. numbers it gives (1.31).
- Mark ✏️ wherever the user should sketch or write their own line.
- Keep quotes short: definitions only.
- Leave out history and digressions, or list them under "skip".
- Link other topics by relative path.

## Don'ts
- Don't write finished prose notes. The handwriting is the user's.
- Don't run heavy OCR on the laptop. Use orca (see `CLAUDE.md`).
- Don't edit `Books/raw`, `Books/text` or `Assignments`.
- Don't start backlog items (listed in `CLAUDE.md`) unless the user asks.
