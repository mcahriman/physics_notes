#!/bin/bash
# page.sh <volume 1|2|3> <printed page> [render]
# Prints the OCR text file for a printed textbook page; with "render", also writes a PNG of
# that page (150 dpi) to the scratch dir given by $OUT (default /tmp) and prints its path.
set -e
ROOT=$(cd "$(dirname "$0")/../../../.." && pwd)
v=$1; p=$2
[ -z "$v" ] || [ -z "$p" ] && { echo "usage: page.sh <vol> <page> [render]"; exit 1; }
n=$((p / 2 + 1)); side=$([ $((p % 2)) -eq 0 ] && echo L || echo R)
f=$ROOT/Books/text/kucheruk$v/$(printf %03d $n)$side.txt
echo "$f"
if [ "$3" = render ]; then
  pdf=$ROOT/Books/raw/kucheruk$v.pdf
  read pw ph < <(pdfinfo "$pdf" | awk '/Page size/{print $3, $5}')
  W=$(awk -v w=$pw 'BEGIN{printf "%d", w*150/72/2 + 1}'); H=$(awk -v h=$ph 'BEGIN{printf "%d", h*150/72 + 1}')
  x=$([ $side = L ] && echo 0 || echo $((W - 1)))
  out=${OUT:-/tmp}/k${v}_p${p}
  pdftoppm -r 150 -gray -png -singlefile -x $x -y 0 -W $W -H $H -f $n -l $n "$pdf" "$out"
  echo "$out.png"
fi
