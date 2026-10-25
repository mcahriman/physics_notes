# Physics notes · Конспекти з загальної фізики

Study wiki and lecture-note scaffolds for a general physics course, built from the textbook
**І. М. Кучерук, І. Т. Горбачук, П. П. Луцик. *Загальний курс фізики*** (т. 1–3). The notes themselves are written by hand; this repository holds everything that supports them.

📄 **[Book/physics-notes.pdf](Book/physics-notes.pdf)**: the whole wiki compiled into one 103-page book.

| Syllabus | Questions | Pages | Status |
|---|---|---|---|
| [Електростатика + постійний струм](wiki/syllabi/electrostatics.md) | 23 | 21 | all formulas checked against the scans |
| [МКР №2 Молекулярна фізика та термодинаміка](wiki/syllabi/mkr2-molecular.md) | 30 | 23 | all formulas checked against the scans |

Start at **[wiki/index.md](wiki/index.md)**.

## Contents

```
wiki/                     the study wiki (Karpathy "LLM wiki" pattern)
  index.md                catalog: start here
  syllabi/                assignment questions → topic pages
  topics/electrostatics/  one page per question: exact textbook terms, formulas with eq. numbers, page refs
  topics/molecular/
  concepts/               ideas that cut across topics (integral↔differential, superposition, processes, transport)
  sources/                chapter/§ → page maps for т. 1–3
  glossary.md             ~100 terms: Ukrainian (as in the book), formula, English, page
  log.md                  history of the work
Book/                     wiki → LuaLaTeX → physics-notes.pdf (build.py, make.sh)
Books/text/               OCR of the three textbook volumes (Tesseract ukr+eng), one file per printed page
Books/download.sh         fetches the textbook scans (not in git) into Books/raw/
Books/tools/ocr.sh        local OCR script
Assignments/              syllabus as given (electrostatics question list)
CLAUDE.md                 working agreement / wiki schema for Claude Code
.claude/                  Claude Code skill (physics-wiki: lookup scripts, workflows) and glossary-validator agent
```

OCR file names: printed page *p* is in `Books/text/kucheruk<vol>/NNN{L,R}.txt`, with NNN = ⌊p/2⌋ + 1, even pages L and odd pages R.
Lookup helper: `.claude/skills/physics-wiki/scripts/page.sh <vol> <page> [render]`.

## Getting the textbook scans

The scanned PDFs are not stored in the repository. Fetch them with

```bash
Books/download.sh             # the three Кучерук volumes → Books/raw/ (checksum-verified)
Books/download.sh --library   # plus the rest of the reading list below → Books/library/
```

## Building the PDF

```bash
Book/make.sh
```

It converts the wiki with `Book/build.py` and compiles with LuaLaTeX in a docker image (`physics-tex`: Ubuntu 24.04 + texlive-luatex, texlive-lang-cyrillic, texlive-latex-extra, fonts-dejavu) on a build host. Edit `make.sh` to change the host, or run `lualatex physics-notes.tex` twice anywhere that has those packages.

## Reading list

Links as provided by the course.

**Основний підручник**
- [І. М. Кучерук, І. Т. Горбачук, П. П. Луцик. Загальний курс фізики. т. 1. Механіка. Молекулярна фізика і термодинаміка. 1999](https://drive.google.com/file/d/19uhoPMBwppprxBSnwpxsMrh9Ef8e4B1I/view?usp=drive_link)
- [І. М. Кучерук, І. Т. Горбачук, П. П. Луцик. Загальний курс фізики. т. 2. Електрика і магнетизм. 1999](https://drive.google.com/file/d/1TRVxqHhyCZrrGaBDl2AVPOMbfae3huvV/view?usp=drive_link)
- [І. М. Кучерук, І. Т. Горбачук, П. П. Луцик. Загальний курс фізики. т. 3. Оптика. Квантова фізика. 1999](https://drive.google.com/file/d/104esSlty3Vaa5wPoMESn34nZPP8M0dp8/view?usp=drive_link)

**Українською**
- [Г. Ю. Лаванов, Г. Б. Бордюг, І. А. Сліпухіна. Фізика. Теорія похибок. — К.: НАУ, 2012](http://physics.zfftt.kpi.ua/repository/coursefilearea/file.php/1/Labs/Errors/Pogreshnosti.pdf)
- [І. Білинський. Теорія ядра та процеси в ньому. 2021](https://drive.google.com/file/d/1Q9A9wmy8rSDsYLBrnzqTnGmQroiijyq0/view?usp=drive_link)
- [І. М. Каденко, В. А. Плюйко. Фізика атомного ядра та частинок. 2019](https://drive.google.com/file/d/1N-BbEOiL6VxUQS1abGdUd8ItxPNmGuj5/view?usp=drive_link)
- [Д. В. Савченко. Методичні вказівки до виконання лабораторних робіт з навчальних дисциплін «Загальна фізика. Частина 1», «Загальна фізика. Частина 2». КПІ ім. Ігоря Сікорського, 2023](http://physics.zfftt.kpi.ua/repository/coursefilearea/file.php/1/Labs/Errors/%D0%A1%D0%B0%D0%B2%D1%87%D0%B5%D0%BD%D0%BA%D0%BE.pdf)
- [А. Г. Бовтрук, Ю. Т. Герасименко, О. В. Грідякіна та ін.; за заг. ред. А. П. Поліщука. Фізика. Механіка. Молекулярна фізика й термодинаміка. 2017](https://drive.google.com/file/d/1UerpRfMoilS7M2EoEhvkAmNBGmV464oY/view?usp=drive_link)
- [Ю. І. Горобець та ін. Фізика. Механіка. 2018](https://drive.google.com/file/d/1scZb30R4xpkrGtSPa_eOz5z_TEBZyijc/view?usp=drive_link)
- [В. М. Дубовик, В. М. Сухов. Лекції з механіки. 2019](https://drive.google.com/file/d/15-w4tbVpilVpgJjmM-3cFrD7L-ptyhva/view?usp=drive_link)
- [Л. А. Булавін, Д. А. Гаврющенко, В. М. Сисоєв. Молекулярна фізика. 2006](https://drive.google.com/file/d/1Q9A9wmy8rSDsYLBrnzqTnGmQroiijyq0/view?usp=drive_link) ⚠️ the source list gives this the same file as Білинський above
- [М. В. Андріяшик, Б. І. Вербицький, А. М. Король. Фізика. Модульно-рейтингова система навчання. 2008](https://drive.google.com/file/d/1nBlmpAWurzihaJ9-kH88e2spfWoG370m/view?usp=drive_link)
- [А. Бурий, О. Цогла. Інноваційне та традиційне у педагогічних технологіях навчання фізики й астрономії в сучасній українській школі. 2022](https://drive.google.com/file/d/1faIBevPzo84gDqHk2WETSbeu_l1zMmSH/view?usp=drive_link)
- [С. І. Долгих. Розвиток компетентностей на уроках астрономії. 2020](https://drive.google.com/file/d/1c-EWIVM2Fj9BvaTG7Wc3AmV8AN8C8Y2t/view?usp=drive_link)
- [І. Крячко. Методика навчання астрономії в старшій загальноосвітній школі. 2018](https://drive.google.com/file/d/1npcSbgQhMDlDoW9jQ5Ag1vfSJFB9QO7X/view?usp=drive_link)
- [Л. Дідух. Електрика і магнетизм. 2021](https://drive.google.com/file/d/1XU854lJI2sVhNrbNyUpPcqSTTNnRtv_K/view?usp=drive_link)

**Іродов**
- [Задачи по общей физике](https://drive.google.com/file/d/11j5ThdPxAkYh3LNM1G0IAxSo3V2DeL9R/view?usp=drive_link)
- [Основные законы механики](https://drive.google.com/file/d/1L9HCZojzzaEjKIiW1v8sY02zfQk2NN6F/view?usp=drive_link)
- [Основные законы электромагнетизма](https://drive.google.com/file/d/1ZwFmClToVRBNRETvx2WO5T3Y8NDyZa-N/view?usp=drive_link)
- [Волновые процессы. Основные законы](https://drive.google.com/file/d/1_b35YNelav165Vr_-oCv94Y4dZ2M41XY/view?usp=drive_link)
- [Квантовая физика. Основные законы](https://drive.google.com/file/d/1-CcP7JJsSN9v1ieAqcre8iEcpNC61dzx/view?usp=drive_link)
- [Физика макросистем. Основные законы](https://drive.google.com/file/d/1AfjUn0bvJegO2Lixanupmdcq8ZLNShSM/view?usp=drive_link)

**Берклеевский курс физики**
- [Ч. Киттель, У. Найт, М. Рудерман. Механика](https://drive.google.com/file/d/1N08fDOVkuieKFM5-jClEdleAsO_dkjQm/view?usp=drive_link)
- [Э. Парселл. Электричество и магнетизм](https://drive.google.com/file/d/1pPv0HqS8o0UfJNeJ1NO1m5YcY0pt4wKq/view?usp=drive_link)
- [Ф. Крауфорд. Волны](https://drive.google.com/file/d/14Om9yipBAQ3JXHA26HHaySRRDg3Ngp2J/view?usp=drive_link) (the source link joined two URLs; this is the second one, as the first is Парселл)
- [Э. Вихман. Квантовая физика](https://drive.google.com/file/d/10TD_ASpGpoEmq9T4t4Tu6uYHWk_QnT7X/view?usp=drive_link)
- [Ф. Рейф. Статистическая физика](https://drive.google.com/file/d/1epAp5nrtQcfAG_T8C8xQN2qeKAcawDF7/view?usp=drive_link)

**Ландау, Лифшиц. Теоретическая физика**
- [т. I. Механика](https://drive.google.com/file/d/1WxKbVcKr1ByX6ztuq9sILg7C1BBi9qpk/view?usp=drive_link)
- [т. III. Квантовая механика (нерелятивистская теория)](https://drive.google.com/file/d/13ISO5WZBk0BnF3mSp8xEPDur0pGuf0zl/view?usp=drive_link)
- [т. IV. Квантовая электродинамика](https://drive.google.com/file/d/1R5iC9-gdoIXhAgiaD1J3a2x6msOayuVu/view?usp=drive_link)
- [т. V. Статистическая физика](https://drive.google.com/file/d/1sMEH_8QviSOd6ZGu4oS7AkRoNG8cvPnq/view?usp=drive_link) · [English: Statistical Physics, v. 5](https://drive.google.com/file/d/1kWFrr_VXctuBBBsldea8tCbkM4nOu4uN/view?usp=drive_link)
- [т. VI. Гидродинамика](https://drive.google.com/file/d/1VPwrB1ZdT_pVScsiVcu0BGnwrYcwsIdm/view?usp=drive_link)
- [т. VII. Теория упругости](https://drive.google.com/file/d/1L1Y4bWnbn1LUjLDVuzEdR897HT8OXqqH/view?usp=drive_link)
- [т. VIII. Электродинамика сплошных сред](https://drive.google.com/file/d/1T6m7wPtD3hZf3sJjQtKyZwMuSYz6xsP4/view?usp=drive_link)
- [т. IX. Статистическая физика, ч. 2. Теория конденсированного состояния](https://drive.google.com/file/d/1f8Ku08ZcsnwZhsBRcIwX-3GADGExPsjh/view?usp=drive_link)
- [т. X. Физическая кинетика](https://drive.google.com/file/d/1G5ovI483uw8VrIkCtIlMjfRyYfG84E5d/view?usp=drive_link)

**Інше**
- [I. P. Bazarov. Thermodynamics. 1964](https://drive.google.com/file/d/1bycQY0134kXnxtU70VoTKDjLOdgu6Mfe/view?usp=drive_link)
- Физическая энциклопедия: [т. 1](https://drive.google.com/file/d/1Z26ievsQ8imyBtrWa4UY7KEVlycOxT0U/view?usp=drive_link) · [т. 2](https://drive.google.com/file/d/1TfAFQGNlA_qWAnWpbQs3KMR-B5-r7CC2/view?usp=drive_link) · [т. 3](https://drive.google.com/file/d/182TD5b0yDueJB91qkst2Nk1Yyg8w0WM_/view?usp=drive_link) · [т. 4](https://drive.google.com/file/d/11fs8lJ5fbq7Mnqxf_zQSANYTF2tVtHJi/view?usp=drive_link) · [т. 5](https://drive.google.com/file/d/1ITThERM3gaXAR-rV7lVN_1-sbztdgS7S/view?usp=drive_link)
- [Г. Горелик. Кто изобрёл современную физику](https://drive.google.com/file/d/1aUkHqWuu0RcqRzETZneBr6-pHhkgoXvq/view?usp=drive_link)
- [Т. И. Трофимова, А. В. Фирсов. Курс физики. Задачи и решения. 2011](https://drive.google.com/file/d/1SWYUOarDUNHqXYoGcuehnfQRcG64ukhF/view?usp=drive_link)
