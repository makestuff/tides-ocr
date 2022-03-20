#!/bin/bash
years="2016 2017 2018 2019 2020 2021 2022"
if [ $# -eq 1 ]; then
  years=$1
fi

for y in ${years}; do
  echo $y
  rm -rf $y
  mkdir $y
  for i in {0..47}; do
    png="${y}/$(printf "%02d" $i).png"
    page=$((39 + $i))
    echo "  ${png}..."
    convert -density 1600 -trim ${y}.pdf[${page}] -rotate 90 +repage ${png}
  done
  echo
done
