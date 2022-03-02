#!/bin/bash
shopt -s nullglob

for filename in $1/*.mov; do
  out="$1/$(basename "$filename" .mov).gif"
  if [ ! -f $out ]; then
    ffmpeg \
      -y \
      -v 0 \
      -i $filename \
      -r 15 \
      -vf scale=512:-1 \
      $out
    fi
done
