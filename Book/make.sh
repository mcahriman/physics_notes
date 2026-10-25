#!/bin/bash
# Build Book/physics-notes.pdf from the wiki.
# Converts wiki/ -> LaTeX locally, compiles on the host `orca` in the docker image
# `physics-tex` (LuaLaTeX + Cyrillic + DejaVu; the laptop has no TeX), fetches the PDF and log.
set -e
cd "$(dirname "$0")"
python3 -I build.py
ssh orca 'mkdir -p ~/physics-book'
scp -q physics-notes.tex orca:physics-book/
ssh orca 'cd ~/physics-book && for i in 1 2; do
  docker run --rm -u $(id -u):$(id -g) -e HOME=/tmp -v $PWD:/w -w /w physics-tex \
    lualatex -interaction=nonstopmode -halt-on-error physics-notes.tex > build.log 2>&1 || { tail -30 build.log; exit 1; }
done'
scp -q orca:physics-book/physics-notes.pdf orca:physics-book/physics-notes.log .
echo "pages: $(pdfinfo physics-notes.pdf | awk '/^Pages/{print $2}')"
echo "errors: $(grep -c '^!' physics-notes.log || true)  missing chars: $(grep -c 'Missing character' physics-notes.log || true)  overfull: $(grep -c 'Overfull' physics-notes.log || true)"
