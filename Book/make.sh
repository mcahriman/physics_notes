#!/bin/bash
# Build Book/physics-notes.pdf from wiki/ (or Book/physics-notes-uk.pdf from wiki-uk/ with: make.sh uk).
# Converts wiki/ -> LaTeX locally, compiles on the host `orca` in the docker image
# `physics-tex` (LuaLaTeX + Cyrillic + DejaVu; the laptop has no TeX), fetches the PDF and log.
set -e
cd "$(dirname "$0")"
LANG_ARG=${1:-}
STEM=physics-notes${LANG_ARG:+-$LANG_ARG}
python3 -I build.py $LANG_ARG
ssh orca 'mkdir -p ~/physics-book'
scp -q $STEM.tex orca:physics-book/
ssh orca "cd ~/physics-book && for i in 1 2; do
  docker run --rm -u \$(id -u):\$(id -g) -e HOME=/tmp -v \$PWD:/w -w /w physics-tex \\
    lualatex -interaction=nonstopmode -halt-on-error $STEM.tex > build.log 2>&1 || { tail -30 build.log; exit 1; }
done"
scp -q orca:physics-book/$STEM.pdf orca:physics-book/$STEM.log .
echo "pages: $(pdfinfo $STEM.pdf | awk '/^Pages/{print $2}')"
echo "errors: $(grep -c '^!' $STEM.log || true)  missing chars: $(grep -c 'Missing character' $STEM.log || true)  overfull: $(grep -c 'Overfull' $STEM.log || true)"
