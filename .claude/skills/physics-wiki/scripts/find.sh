#!/bin/bash
# find.sh <term> [vol]
# Searches the wiki first (pages that already cover the term), then the OCR text,
# printing printed page numbers for OCR hits so they can be cited.
ROOT=$(cd "$(dirname "$0")/../../../.." && pwd)
t=$1; v=${2:-*}
echo "== wiki"; grep -rli -- "$t" "$ROOT/wiki" | sed "s|$ROOT/||"
echo "== textbook (vol, page: line)"
for f in $ROOT/Books/text/kucheruk$v/*.txt; do
  grep -qi -- "$t" "$f" || continue
  b=$(basename "$f" .txt); n=$((10#${b:0:3})); s=${b:3:1}
  p=$((2 * n - 1)); [ "$s" = L ] && p=$((p - 1))
  vol=$(basename "$(dirname "$f")"); vol=${vol#kucheruk}
  grep -i -m2 -- "$t" "$f" | sed "s|^|т.$vol p.$p: |" | cut -c1-140
done
