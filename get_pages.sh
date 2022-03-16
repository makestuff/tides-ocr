#!/bin/bash
rm -rf pages platidetable2022webversion.pdf
wget https://www.pla.co.uk/assets/platidetable2022webversion.pdf
mkdir -p pages
echo "Extracting ${png}..."
for i in {0..47}; do
  png="pages/$(printf "%02d" $i).png"
  page=$((39 + $i))
  echo "  ${png}..."
  convert -density 1600 -trim platidetable2022webversion.pdf[${page}] -rotate 90 +repage ${png}
done
