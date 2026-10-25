#!/bin/bash
# Usage: ocr.sh <book-stem> <first-spread> <last-spread>
# Splits each landscape spread into left/right pages, OCRs with Tesseract (ukr+eng),
# writes Books/text/<stem>/<spread>L.txt and <spread>R.txt
set -e
export OMP_THREAD_LIMIT=1
export TESSDATA_PREFIX=$HOME/.local/share/tessdata
ROOT=/home/yurii_borysov/Work/Study/Physics/Books
stem=$1; a=$2; b=$3
out=$ROOT/text/$stem; mkdir -p "$out"
one() {
  n=$1; p=$(printf %03d $n)
  [ -s "$out/${p}R.txt" ] && exit 0
  tmp=$(mktemp -d)
  pdftoppm -r 300 -gray -png -x 0 -y 0 -W 1750 -H 2480 -f $n -l $n "$ROOT/raw/$stem.pdf" "$tmp/L"
  pdftoppm -r 300 -gray -png -x 1749 -y 0 -W 1750 -H 2480 -f $n -l $n "$ROOT/raw/$stem.pdf" "$tmp/R"
  mv $tmp/L-*.png $tmp/L.png; mv $tmp/R-*.png $tmp/R.png
  for s in L R; do tesseract "$tmp/$s.png" "$out/$p$s" -l ukr+eng --psm 1 >/dev/null 2>&1; done
  rm -rf "$tmp"
}
export -f one; export out ROOT stem
seq $a $b | xargs -P 7 -I{} bash -c 'one {}'
