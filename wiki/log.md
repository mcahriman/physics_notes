# Log

Append-only. One entry per operation, newest at the bottom. Header format: `## [YYYY-MM-DD] <op> | <subject>`, where op ∈ {setup, ocr, ingest, topic, glossary, verify, query, lint, scope}.
Quick view: `grep "^## \[" wiki/log.md | tail -10`

## [2026-10-25] setup | Project started
- Sources: Кучерук т. 1, 2 (later т. 3) scans in `Books/raw/`. Syllabi in `Assignments/Lecture notest/`.
- Assessment: т. 2 §1.1 is genuinely hard to take notes from. The properties of charge are spread across pp. 14–21 among history and digressions, and the book never lists them.

## [2026-10-25] ocr | All three volumes
- Tesseract `ukr+eng`, spreads split into L/R. Runs on host `orca` in docker `physics-ocr`, because the laptop overheated.
- т. 1: 538 pages, т. 2: 458, т. 3: 522. Printed page p → spread ⌊p/2⌋ + 1 in every volume.
- Found that т. 1 part II = Молекулярна фізика і термодинаміка, the source for МКР №2.

## [2026-10-25] topic | 01 Електричний заряд
- Skeleton plus 15 glossary entries. Formulas (1.1)–(1.5), e, mₑ, r₀ checked against the scan.

## [2026-10-25] topic | 02–23 Електростатика + постійний струм
- Skeletons for all remaining syllabus questions (10–12 merged into one page). Built from the OCR of §1.2–1.14, 1.25–1.26, 2.1–2.6.
- ⚠️ Formulas not yet checked against scans (frontmatter `formulas_checked: false`).

## [2026-10-25] setup | Wiki created (Karpathy LLM-wiki pattern)
- Moved `Notes/` → `wiki/topics/` and `Glossary.md` → `wiki/glossary.md`. Added the index, the log, source maps for т. 1–3, syllabus pages and 2 concept pages.
- Schema: `CLAUDE.md`. Navigation skill: `.claude/skills/physics-wiki/`.

## [2026-10-25] scope | МКР №2 Молекулярна фізика: plan
- The user took the item from the backlog. Mapped all 30 questions to § and pages of т. 1 ch. 14–19, using section headings found in the OCR.
- 30 questions → 22 planned pages (merged: 7–9, 12–13, 17+19, 20–21, 23–25). Study order in blocks A–H. Skip list.
- Terminology differences: «ступені вільності» (not «свободи»), «адіабатний», «Максвелла», «Ван-дер-Ваальса».
- Added the § table for ch. 14–19 to `sources/kucheruk1.md`.

## [2026-10-25] setup | Topics split into per-syllabus folders
- `wiki/topics/*.md` → `wiki/topics/electrostatics/`; `wiki/topics/molecular/` created. All links rewritten; link check: 0 broken.

## [2026-10-25] topic | МКР №2 block A: 02, 01, 20–21
- Pages written in `topics/molecular/` from т. 1 §14.2–14.4, §14.6–14.7, §16.2 (pp. 375–377), §16.5 (pp. 390–392).
- Formulas checked against the scan at write time: (14.5), (14.6), (14.8)–(14.10), (14.14)–(14.18), (16.3), (16.4), (16.46), C_V values. The isoprocess laws (14.22)–(14.31) come from clear OCR.
- 21 glossary entries added (section 3, block A).
- Notes: the book doesn't name the isochoric law after Charles. The book uses both «рівного» and «рівномірного розподілу» (pp. 377, 392).

## [2026-10-25] topic | МКР №2 blocks B–H: all remaining pages
- 19 pages in `topics/molecular/`: 18, 17+19, 22, 23–25, 03, 04, 06, 05, 07–09, 10, 11, 12–13, 16, 14, 15, 26, 27, 28, 29, 30. All 30 questions are now covered on 22 pages.
- Formulas checked against the scan at write time on 17/22 pages. Not checked: 11, 15, 26, 28, 29, 30 (taken from clear OCR; those pages carry `formulas_checked: false`). Table 18.4 (syngonies) in particular needs a scan check.
- New concept pages: `isoprocesses-table`, `transport-phenomena`.
- 63 glossary entries for blocks B–H (99 in total).
- Findings worth knowing:
  - The book's (16.10) text calls d'A the work «над системою». This contradicts its own sign convention (p. 378); the page explains it.
  - The book never says «необернений цикл»; it uses прямий / обернений.
  - The reverse-Carnot ε = T₂/(T₁−T₂) is derived on the page, not quoted from the book.
  - Question 30 «Рідини» was handwritten on the sheet, so its scope is unclear. §19.3–19.4 (surface tension, capillarity) are not covered yet.

## [2026-10-25] proofread | pre-PDF proofreading of topics, concepts, glossary, syllabi, index
- Page count fixed: the molecular section has 23 pages, not 22 (index, syllabus, CLAUDE.md).
- Checked against the scan: т. 1 pp. 335–336, 394, 412, 448, 454–455, 463, 466; т. 2 pp. 23, 25, 33, 35, 43, 47–48, 52, 102, 113, 121, 123.
- Formula fixes: T_пост ≪ T_оберт ≪ T_колив (05); (2.20) is ρ = ρ₀αT (21); τ = Ae^{ΔW/kT} (19.1) and oscillation period 10⁻¹² с (30); n_в, W_в notation in (18.4) (29); the 6-molecule example is in the text on p. 412, not on рис. 16.15 (14); v_кв ratio notation (18).
- The book's (14.73) is misprinted (dh inside the exponent); flagged on 17,19.
- Table 18.4 (28) and the σ exponents (21) confirmed against the scan; quote «у вакуумі» fixed (06); syllabus notation ⟨l⟩/λ aligned with the pages.
- Small wording, unit-letter (Cyrillic А, К) and link fixes; link check: 0 broken.

## [2026-10-25] setup | PDF book
- `Book/build.py` (wiki → LuaLaTeX) and `Book/make.sh` (compiles on orca in docker `physics-tex`). Output: `Book/physics-notes.pdf`, 103 pages: both parts, 4 concept appendices, glossary.
- Opus proofreading pass over the wiki before the build (see the `proofread` entry). A Sonnet pass over the PDF found no must-fix defects. Fixed after it: stray rules, plain-text subscripts, long running headers, an orphaned heading.
- Known cosmetic issues: the ASCII layout boxes have ragged right edges (hand-drawn in the source), and the 9-column process table is cramped.

## [2026-10-25] verify | Scan check of all remaining pages
- Electrostatics 02–23: every formula checked against т. 2 pp. 21–131. Molecular 11, 15, 26, 28, 29, 30: checked against т. 1 pp. 397–399, 414–415, 419–421, 446–448, 453–456, 462–467. All 44 topic pages now have `formulas_checked: true`.
- Two **misprints in the book**, flagged on the pages (the wiki forms are correct):
  - (1.37), p. 40: printed E = η/(4πε₀r), should be η/(2πε₀r) (page 10–12);
  - (1.60), p. 51: printed φ₁ − φ₂ = −∫E dl, which contradicts (1.53) and (1.59) (page 08).
- Wiki fix: page 23, w = ρj² is (2.48) and w = σE² is (2.49); they were both labelled (2.49).
- Index, both syllabus status tables and CLAUDE.md updated.

## [2026-10-25] setup | Ukrainian-first edition
- `wiki-uk/`: all 44 topic pages, 4 concepts, both syllabi and the glossary translated into Ukrainian. English equivalents of key terms are kept as «(англ. …)», and the glossary uses «(англ.)». Formulas, eq. numbers, page refs and quotes are unchanged.
- `Book/build.py uk` / `Book/make.sh uk` → `Book/physics-notes-uk.pdf` (103 pages, 0 errors, 0 missing glyphs).
- New agent `translation-proofreader` (`.claude/agents/`) checks `wiki-uk/` against `wiki/`.
