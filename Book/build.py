#!/usr/bin/env python3
"""Compile the study wiki (wiki/) into one LuaLaTeX book: Book/physics-notes.tex.

Handles only the Markdown subset the wiki uses: YAML frontmatter, #/## headings,
paragraphs, -/1. lists (one nesting level), pipe tables, ``` code blocks, **bold**,
***bold italic***, `code`, [links](...), $inline$ and $$display$$ math.
Build the PDF with:  lualatex physics-notes.tex  (twice, for the table of contents).
With the argument "uk" it reads the Ukrainian-first wiki (wiki-uk/) and writes physics-notes-uk.tex.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANG = "uk" if "uk" in sys.argv[1:] else "en"
WIKI = ROOT / ("wiki-uk" if LANG == "uk" else "wiki")
OUT = Path(__file__).resolve().parent / ("physics-notes-uk.tex" if LANG == "uk" else "physics-notes.tex")

ELECTRO = sorted((WIKI / "topics/electrostatics").glob("*.md"))
# Molecular pages in the study order of the plan (blocks A–H), not syllabus order.
MOLECULAR_ORDER = ["02", "01", "20-21", "18", "17,19", "22", "23-25", "03", "04", "06", "05",
                   "07-09", "10", "11", "12-13", "16", "14", "15", "26", "27", "28", "29", "30"]
MOLECULAR = [next((WIKI / "topics/molecular").glob(k + "_*.md")) for k in MOLECULAR_ORDER]
CONCEPTS = ["integral-vs-differential", "superposition", "isoprocesses-table", "transport-phenomena"]

EMOJI = {
    "✏️": r"\pen{}", "✏": r"\pen{}", "⚠️": r"\warn{}", "⚠": r"\warn{}", "✅": r"\ok{}",
    "⚡": r"\spark{}", "📖": r"\book{}", "📝": "", "✍️": "", "🟢": "", "🟡": "", "⚪": "", "⬜": "",
}
CYR = "А-Яа-яІіЇїЄєҐґ'’"


def esc_text(s):
    """Escape LaTeX specials in plain text (no math inside)."""
    s = s.replace("\\", r"\textbackslash{}")
    for a, b in [("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("{", r"\{"), ("}", r"\}"),
                 ("~", r"\textasciitilde{}")]:
        s = s.replace(a, b)
    # identifier_subscript and identifier^power written as plain text -> math.
    # The math is parked in placeholders so the underscore escaping below can't touch it.
    maths = []

    def park(tex):
        maths.append("$" + tex + "$")
        return "\x02%d\x03" % (len(maths) - 1)

    s = re.sub(r"(?<![A-Za-z0-9_\\])([A-Za-zεηλσρφωγτνθΔδπ]+)_\{?([A-Za-z" + CYR + r"0-9.−+]+)\}?",
               lambda m: park(m.group(1) + "_{" + cyr_text(m.group(2)) + "}"), s)
    s = re.sub(r"(?<![\w\\])([A-Za-z]+)\^\(([^)]*)\)", lambda m: park(m.group(1) + "^{" + cyr_text(m.group(2)) + "}"), s)
    s = re.sub(r"(?<![\w\\])([A-Za-z]+)\^([A-Za-zγ0-9.−]+)", lambda m: park(m.group(1) + "^{" + cyr_text(m.group(2)) + "}"), s)
    s = s.replace("_", r"\_").replace("^", r"\textasciicircum{}")
    return re.sub(r"\x02(\d+)\x03", lambda m: maths[int(m.group(1))], s)


def cyr_text(m):
    """Inside math: wrap runs of Cyrillic letters in \\text{} (math fonts lack Cyrillic)."""
    return re.sub(r"[" + CYR + r"]+(?:[ " + CYR + r"]*[" + CYR + r"])?", lambda x: r"\text{" + x.group(0) + "}", m)


def inline(s):
    """Convert one line/cell of Markdown inline syntax to LaTeX."""
    for k, v in EMOJI.items():
        s = s.replace(k, "\x00" + v + "\x01")
    s = s.replace("\ufe0f", "")
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)          # links -> text
    out, i = [], 0
    # split into math / code / text segments
    pattern = re.compile(r"\$\$(.+?)\$\$|\$(.+?)\$|`([^`]+)`")
    for m in pattern.finditer(s):
        out.append(("t", s[i:m.start()]))
        if m.group(1) is not None:
            out.append(("dm", m.group(1)))
        elif m.group(2) is not None:
            out.append(("m", m.group(2)))
        else:
            out.append(("c", m.group(3)))
        i = m.end()
    out.append(("t", s[i:]))
    res = []
    for kind, seg in out:
        if kind == "t":
            parts = re.split(r"(\x00.*?\x01)", seg)
            t = "".join(p[1:-1] if p.startswith("\x00") else esc_text(p) for p in parts)
            t = re.sub(r"\*\*\*(.+?)\*\*\*", r"\\textbf{\\textit{\1}}", t)
            t = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", t)
            t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\\textit{\1}", t)
            res.append(t)
        elif kind == "m":
            res.append("$" + cyr_text(seg) + "$")
        elif kind == "dm":
            res.append(r"\[" + cyr_text(seg) + r"\]")
        else:
            res.append(r"\texttt{" + esc_text(seg).replace("$", r"\$") + "}")
    t = "".join(res)
    # bold markers that span a math segment were split above; fix the common case
    t = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", t)
    return t


def table(rows):
    """Pipe-table rows -> longtable with p-columns sized by content length."""
    cells = [[re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", c.strip()) for c in r.strip().strip("|").split("|")]
             for r in rows]
    head, body = cells[0], [r for r in cells[2:]]
    n = len(head)
    body = [r + [""] * (n - len(r)) for r in body]
    lens = [max([len(head[j])] + [len(r[j]) for r in body]) for j in range(n)]
    lens = [min(max(l, 4), 60) for l in lens]
    size = r"\footnotesize" if n >= 5 else r"\small"
    if n >= 8:
        size = r"\scriptsize"
    char = {r"\scriptsize": 0.0095, r"\footnotesize": 0.0115, r"\small": 0.013}[size]
    # a column must fit its longest unbreakable word (math/code counted as one word)
    def longest_word(c):
        c = re.sub(r"\$[^$]*\$", lambda m: "x" * max(2, len(m.group(0)) // 2), c)
        return max([len(w) for w in re.split(r"[\s/]+", c)] + [1])
    mins = [char * max([longest_word(head[j])] + [longest_word(r[j]) for r in body]) for j in range(n)]
    avail = 1.0 - 0.016 * n
    total = sum(lens)
    widths = [max(avail * l / total, m) for l, m in zip(lens, mins)]
    if sum(mins) >= avail:                       # can't satisfy every minimum: scale them
        widths = [m * avail / sum(mins) for m in mins]
    elif sum(widths) > avail:                    # shrink only the columns above their minimum
        extra = sum(widths) - avail
        slack = [w - m for w, m in zip(widths, mins)]
        widths = [w - extra * s / sum(slack) for w, s in zip(widths, slack)]
    else:
        widths = [w * avail / sum(widths) for w in widths]
    spec = "".join(r">{\raggedright\arraybackslash}p{%.3f\linewidth}" % w for w in widths)
    lines = ["{" + size, r"\begin{longtable}{" + spec + "}", r"\toprule",
             " & ".join(r"\textbf{" + inline(h) + "}" for h in head) + r" \\", r"\midrule", r"\endhead"]
    for r in body:
        lines.append(" & ".join(inline(c) for c in r[:n]) + r" \\")
    lines += [r"\bottomrule", r"\end{longtable}", "}"]
    return "\n".join(lines)


def body(md, level_offset=0):
    """Convert a page body (frontmatter already removed) to LaTeX."""
    lines = md.split("\n")
    out, i, list_stack = [], 0, []

    def close_lists(to=0):
        while len(list_stack) > to:
            out.append(r"\end{" + list_stack.pop() + "}")

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith("```"):
            close_lists()
            j = i + 1
            block = []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                block.append(lines[j])
                j += 1
            out.append(r"\begin{layout}")
            out += block
            out.append(r"\end{layout}")
            i = j + 1
            continue
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            close_lists()
            j = i
            rows = []
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append(lines[j])
                j += 1
            out.append(table(rows))
            i = j
            continue
        if not s:
            close_lists()
            out.append("")
            i += 1
            continue
        if s == "---":
            close_lists()
            out.append(r"\par\noindent{\color{accent!30}\rule{\linewidth}{0.4pt}}\par")
            i += 1
            continue
        if s.startswith("[←") or s.startswith("[index]"):
            i += 1
            continue
        m = re.match(r"^(#{2,4})\s+(.*)", s)
        if m:
            close_lists()
            lvl = len(m.group(1)) + level_offset
            cmd = {2: "section*", 3: "subsection*", 4: "subsubsection*"}.get(lvl, "paragraph")
            out.append(r"\needspace{5\baselineskip}" + "\\" + cmd + "{" + inline(m.group(2)) + "}")
            i += 1
            continue
        m = re.match(r"^(\s*)(-|\d+\.)\s+(.*)", ln)
        if m:
            depth = len(m.group(1)) // 2 + 1
            kind = "itemize" if m.group(2) == "-" else "enumerate"
            while len(list_stack) > depth:
                out.append(r"\end{" + list_stack.pop() + "}")
            if len(list_stack) < depth:
                list_stack.append(kind)
                out.append(r"\begin{" + kind + "}")
            out.append(r"\item " + inline(m.group(3)))
            i += 1
            continue
        if list_stack and ln.startswith("  "):          # continuation inside a list item
            out.append(inline(s))
            i += 1
            continue
        close_lists()
        if s.startswith("📖"):
            out.append(r"\srcline{" + inline(s) + "}")
        else:
            out.append(inline(s))
        i += 1
    close_lists()
    return "\n".join(out)


def page(path, kind="chapter"):
    md = path.read_text()
    if md.startswith("---"):
        md = md.split("---", 2)[2]
    md = md.strip("\n")
    first, rest = md.split("\n", 1)
    title = re.sub(r"\s+—\s+каркас.*$", "", first.lstrip("# ").strip())
    return chapter(inline(title)) + "\n" + body(rest)


def chapter(t):
    """Unnumbered chapter (topic titles carry their own syllabus numbers) with TOC entry and header."""
    short = t.split(" · ")[0]
    if len(short) > 60:
        short = short[:57].rsplit(" ", 1)[0] + "…"
    return r"\chapter*{%s}\addcontentsline{toc}{chapter}{%s}\markboth{%s}{%s}" % (t, t, short, short)


def syllabus_intro(path, keep_sections=None):
    """Syllabus page: drop the status column and the bookkeeping sections."""
    md = path.read_text().split("---", 2)[2].strip("\n")
    md = md.split("\n", 1)[1]
    parts = re.split(r"(?m)^(?=## )", md)
    if keep_sections is not None:
        parts = [parts[0]] + [p for p in parts[1:] if any(p.startswith("## " + k) for k in keep_sections)]
    md = "".join(parts)
    # drop status columns ("Status" header and the last cell of table rows)
    new = []
    for ln in md.split("\n"):
        if ln.startswith("|") and "Status" in ln:
            ln = "|".join(ln.split("|")[:-2]) + "|"
        elif ln.startswith("|---") or ln.startswith("|--"):
            pass
        elif re.match(r"^\|.*\| (📝✅|📝|⬜|✍️)+ \|$", ln):
            ln = "|".join(ln.split("|")[:-2]) + "|"
        new.append(ln)
    # fix separator rows to match the header width
    out, prev_cols = [], None
    for ln in new:
        if re.match(r"^\|[\s:|-]+\|$", ln.strip()) and prev_cols:
            ln = "|" + "|".join(["---"] * prev_cols) + "|"
        if ln.startswith("|"):
            prev_cols = len(ln.strip().strip("|").split("|"))
        out.append(ln)
    md = "\n".join(out)
    md = re.sub(r"(?m)^Status:.*\n", "", md)
    md = re.sub(r"(?m)^The assignment is handwritten.*\n", "", md)
    return body(md)


PREAMBLE = r"""\documentclass[11pt,a4paper,oneside]{book}
\usepackage[margin=20mm,top=22mm,bottom=22mm]{geometry}
\usepackage{fontspec}
\usepackage{amsmath}
\usepackage[math-style=ISO]{unicode-math}
\usepackage{polyglossia}
\setdefaultlanguage{ukrainian}
\setotherlanguage{english}
\directlua{
  luaotfload.add_fallback("fallbacks", {"DejaVu Sans:mode=harf;", "FreeSerif:mode=harf;", "DejaVu Math TeX Gyre:mode=harf;"})
}
\setmainfont{DejaVu Serif}[RawFeature={fallback=fallbacks}]
\setsansfont{DejaVu Sans}[RawFeature={fallback=fallbacks}]
\setmonofont{DejaVu Sans Mono}[Scale=0.85,RawFeature={fallback=fallbacks}]
\setmathfont{DejaVu Math TeX Gyre}
\usepackage{microtype}
\usepackage{needspace}
\usepackage{booktabs,longtable,array}
\usepackage{enumitem}
\setlist{nosep,leftmargin=*}
\usepackage{xcolor}
\definecolor{accent}{HTML}{1F4E79}
\definecolor{warncol}{HTML}{B45309}
\usepackage{titlesec}
\titleformat{\chapter}[hang]{\Large\bfseries\sffamily\color{accent}}{\thechapter.}{0.6em}{}
\titlespacing*{\chapter}{0pt}{-10pt}{10pt}
\titleformat{\section}{\normalsize\bfseries\sffamily\color{accent}}{}{0pt}{}
\titlespacing*{\section}{0pt}{8pt}{3pt}
\titleformat{\part}[display]{\centering\Huge\bfseries\sffamily\color{accent}}{\partname~\thepart}{12pt}{}
\usepackage{fancyhdr}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small\sffamily\leftmark}\fancyhead[R]{\small\sffamily\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\usepackage{fancyvrb}
\DefineVerbatimEnvironment{layout}{Verbatim}{fontsize=\footnotesize,frame=single,framesep=2mm,rulecolor=\color{accent!40}}
\usepackage[hidelinks,unicode]{hyperref}
\newcommand{\pen}{{\sffamily\color{accent}✎}}
\newcommand{\warn}{{\sffamily\color{warncol}⚠}}
\newcommand{\ok}{{\sffamily\color{green!45!black}✔}}
\newcommand{\spark}{{\sffamily\color{warncol}⚡}}
\newcommand{\book}{}
\newcommand{\srcline}[1]{\par\noindent{\small\color{black!70}\textit{Джерело:} #1}\par\medskip}
\setlength{\parindent}{0pt}\setlength{\parskip}{3pt}
% Mixed Ukrainian/English text: Ukrainian hyphenation patterns can't break English words,
% so give the line breaker room instead of producing overfull lines.
\setlength{\emergencystretch}{3em}\tolerance=2000
\setlength{\tabcolsep}{3.5pt}
\raggedbottom
"""

FRONT = r"""
\begin{titlepage}
\centering\sffamily
\vspace*{40mm}
{\Huge\bfseries\color{accent} Загальний курс фізики\par}
\vspace{6mm}
{\LARGE Каркаси конспектів лекцій\par}
\vspace{12mm}
{\large Електростатика і постійний струм\\[2mm] Молекулярна фізика і термодинаміка\par}
\vfill
{\normalsize За підручником: Кучерук І.\,М., Горбачук І.\,Т., Луцик П.\,П.\\
\textit{Загальний курс фізики}, т.~1 (1999), т.~2 (2001). — К.: Техніка.\par}
\vspace{8mm}
{\small Згенеровано з вікі проєкту, \today\par}
\end{titlepage}

\chapter*{Як користуватися}
\addcontentsline{toc}{chapter}{Як користуватися}\markboth{Як користуватися}{}
Кожен розділ — це \textbf{каркас} однієї рукописної сторінки конспекту, а не готовий конспект. Він містить:
\begin{itemize}
\item \textbf{@LAYOUT@} — план сторінки у вигляді рамок [A], [B], …;
\item точні терміни й означення з підручника (у «лапках»), формули з номерами рівнянь книги, сторінки;
\item \pen{} — місця, де треба намалювати схему чи сформулювати думку власними словами;
\item \warn{} — розбіжності між підручником і програмою, помилки в книзі, неперевірені місця;
\item \ok{} — формули звірено зі сканом сторінки; \spark{} — важливий або парадоксальний висновок;
\item \textbf{@SELFCHECK@} — 2–4 запитання для самоперевірки.
\end{itemize}
@LANGNOTE@ Посилання «т.~2, с.~38» — друковані сторінки підручника.
"""


def main():
    front = FRONT
    if LANG == "uk":
        front = (front.replace("@LAYOUT@} — план сторінки у вигляді рамок", "План сторінки} — розкладка сторінки на рамки").replace("@SELFCHECK@", "Самоперевірка")
                 .replace("@LANGNOTE@", "Усі пояснення — українською; поруч із ключовими термінами в дужках подано англійські відповідники «(англ. …)». Терміни й цитати — дослівно з підручника."))
    else:
        front = (front.replace("@LAYOUT@", "Layout").replace("@SELFCHECK@", "Self-check")
                 .replace("@LANGNOTE@", "Пояснення до структури подано англійською, терміни й цитати — українською, як у підручнику."))
    parts = [PREAMBLE, r"\begin{document}", r"\frontmatter", front, r"\tableofcontents", r"\mainmatter"]
    parts.append(r"\part{Електростатика і постійний струм}")
    parts.append(chapter("Програма: 23 питання"))
    parts.append(syllabus_intro(WIKI / "syllabi/electrostatics.md"))
    for p in ELECTRO:
        parts.append(page(p))
    parts.append(r"\part{Молекулярна фізика і термодинаміка}")
    parts.append(chapter("Програма МКР №2: 30 питань"))
    parts.append(syllabus_intro(WIKI / "syllabi/mkr2-molecular.md", keep_sections=["1.", "2.", "3."]))
    for p in MOLECULAR:
        parts.append(page(p))
    parts.append(r"\appendix")
    parts.append(r"\part{Додатки}")
    for c in CONCEPTS:
        parts.append(page(WIKI / f"concepts/{c}.md"))
    g = (WIKI / "glossary.md").read_text().split("---", 2)[2]
    g = g.split("\n## 1.", 1)[1]
    parts.append(chapter("Глосарій") + "\n" + body("## 1." + g))
    parts.append(r"\end{document}")
    OUT.write_text("\n\n".join(parts) + "\n")
    print("wrote", OUT, sum(1 for _ in ELECTRO), "+", len(MOLECULAR), "topic pages")


if __name__ == "__main__":
    main()
