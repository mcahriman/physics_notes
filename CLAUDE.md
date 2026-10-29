# Physics lecture notes — wiki schema and working agreement

The user writes lecture notes **by hand**. Claude maintains a study wiki that supports this: it finds the exact Ukrainian terms, structures each syllabus question as a one-page scaffold, and keeps the glossary, source maps and cross-links up to date. **Do not write finished notes.** The project runs for at least a year, so keep the wiki consistent and navigable.

Pattern: Karpathy's LLM wiki (https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). There are three layers: raw sources (immutable) → `wiki/` (maintained by Claude) → this file (the schema). The workflows (query / ingest / lint), page templates and lookup scripts are in the **`physics-wiki` skill** (`.claude/skills/physics-wiki/`). Load it for any wiki work.

## Layout

```
Books/raw/kucheruk{1,2,3}.pdf    scans (immutable; NOT in git, fetch with Books/download.sh)
Books/text/kucheruk{1,2,3}/      OCR, NNN{L,R}.txt per printed page (derived, don't hand-edit)
Books/tools/ocr.sh               local OCR (max 2 parallel jobs)
Books/download.sh                fetches the scans (+ --library: the course reading list) from the links in README.md
Assignments/Lecture notest/      syllabi as given (immutable)
wiki/index.md                    catalog: read first, update on every change
wiki/log.md                      append-only: "## [YYYY-MM-DD] <op> | <subject>"
wiki/syllabi/                    assignment → topic pages + status
wiki/topics/<syllabus>/NN_*.md   one scaffold per syllabus question (electrostatics/, molecular/)
wiki/concepts/                   cross-topic ideas
wiki/sources/kucheruk{1,2,3}.md  chapter/§ → pages → spreads → topics
wiki/glossary.md                 exact terms, formula, EN, page
wiki-uk/                         Ukrainian-first mirror of wiki/ (topics, concepts, syllabi, glossary) for the uk book
.claude/skills/physics-wiki/     navigation skill + scripts (page.sh, find.sh)
.claude/agents/glossary-validator.md   checks the glossary against the scans
.claude/agents/translation-proofreader.md   checks wiki-uk/ against wiki/
Book/build.py, Book/make.sh        wiki -> one LuaLaTeX book -> Book/physics-notes.pdf (./make.sh) or physics-notes-uk.pdf (./make.sh uk)
```

## Sources

- Кучерук et al., *Загальний курс фізики*: т. 1 Механіка + **Молекулярна фізика і термодинаміка** (part II, ch. 13–22); т. 2 Електрика і магнетизм; т. 3 Оптика + Квантова фізика.
- Each PDF page is a landscape spread of two printed pages. **Printed page p → spread ⌊p/2⌋ + 1, even = L, odd = R**, in all three volumes. Use `page.sh <vol> <p>`.
- The OCR (Tesseract `ukr+eng`) is good for prose but garbles formulas, drop caps and exponents. **Check the scan before quoting any formula or exact definition.** Topic frontmatter records `formulas_checked`.

## Conventions

- Page names are Ukrainian and match the syllabus wording. Links are relative markdown links (`[text](../topics/…md)`), so they work in the app and in Obsidian.
- Every wiki page has YAML frontmatter (`type`, `updated`, …) and a nav line under the title.
- Every concept is defined once and linked from elsewhere. Every claim from the book carries a page ref (`т. 2, с. 38`).
- Book blocks [A]–[F] hold only what the book prints. Our own shorthand, rewritten forms and derivations go to `## Addendum (not in the book)` (uk: `## Доповнення (не з книги)`) at the very bottom of the page, after the self-check. Each item points back to its block (→ [C]).
- Terms are written exactly as the book has them, e.g. «теорема Гаусса» with double с, even where the syllabus writes «Гауса».
- After any change: update `wiki/index.md` and the syllabus status, and append to `wiki/log.md`.

## OCR

Heavy OCR runs on the host **`orca`** (`ssh orca`; 24 cores; docker image `physics-ocr`; working dir `~/ocr-physics/`; `ocr_remote.sh <stem> [first] [last]`, which reads the page size from the PDF). It never runs on the laptop, which overheats. Sync with `rsync -a orca:ocr-physics/text/ Books/text/`. Status: all three volumes are fully OCRed (2026-10-25).
Use `pkill -x tesseract`, never a broad `pkill -f`, because the laptop also runs Steam.

## Git

Repository: github.com/mcahriman/physics_notes (**public**). Never commit the scans (`Books/raw/`, `Books/library/`) or the МКР photo (it shows classmates' names); `.gitignore` covers these.

## PDF book

`Book/make.sh` converts the wiki (`Book/build.py`, a converter for the wiki's Markdown subset) and compiles it with LuaLaTeX on **orca** in the docker image `physics-tex` (`~/physics-book/`). Neither the laptop nor orca's own TeX Live can build it: orca lacks luaotfload and Cyrillic support. Rebuild after any wiki change. A clean build reports 0 errors and 0 missing characters; about 7 small overfull lines remain, mostly in the 9-column process table. Keep wiki Markdown inside the subset build.py handles: one list nesting level, `$$…$$` on its own line, pipe tables.

## Ukrainian edition

`wiki-uk/` mirrors the book pages of `wiki/` with all explanations in Ukrainian. Key terms keep English equivalents as «(англ. …)», and the glossary uses «(англ.)». Formulas, equation numbers, page refs and «quotes» are identical to `wiki/`. **`wiki/` is the source of truth:** after changing a page there, update its `wiki-uk/` counterpart, run the `translation-proofreader` agent, then rebuild with `Book/make.sh uk`.

## Scope: now

**Електростатика + постійний струм**: 23 questions, [wiki/syllabi/electrostatics.md](wiki/syllabi/electrostatics.md), т. 2 ch. 1–2. All topic skeletons exist. All 21 pages are formula-checked against the scans.

**Молекулярна фізика та термодинаміка (МКР №2)**: 30 questions, [wiki/syllabi/mkr2-molecular.md](wiki/syllabi/mkr2-molecular.md), т. 1 ch. 14–19 (pp. 298–484). **All 23 skeleton pages are written** (blocks A–H) in `wiki/topics/molecular/`, with 99 glossary entries in total. All pages are formula-checked against the scans. Use the book's terms («ступені вільності», «адіабатний», «Максвелла»). Open question: does МКР question 30 «Рідини» include surface tension (§19.3–19.4)? Ask the user.

## Backlog (do not start until the user says so)

1. Fill the glossary for electrostatics topics 02–23. Only topic 1 has entries so far.
2. т. 2 ch. 3–14 (magnetism, induction, waves): mapped in `wiki/sources/kucheruk2.md`, not studied.
3. т. 1 part I (mechanics) and т. 3 (optics, quantum): mapped only, no syllabus yet.
4. **Demo: partial derivatives** (in the separate math section `demos/math/`, single-file like the others). The user's rule: no physics that uses ∂ without a demo of ∂ first. It should show ∂φ/∂x as the slope along one coordinate with the other held fixed, the total differential dφ = φₓdx + φ_ydy, equal mixed partials, and the subscripted form (∂U/∂T)_V from thermodynamics. `demos/math/grad-div-rot.html` uses partial derivatives without teaching them, so link the new demo as its prerequisite and add it to `demos/index.html`.

When the user takes on a backlog item, move it to "Scope: now", update this file and log it.
