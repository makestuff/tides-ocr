#!/usr/bin/env python3

import tide_ocr
import urllib.request
import os
import sys
import pathlib
import datetime
import json

# Locations given in the tide tables, numbered 0-6
LOCATIONS = [
  "Walton-on-the-Naze",
  "Margate",
  "Shivering Sand",
  "Southend-on-Sea",
  "Tilbury",
  "North Woolwich",
  "London Bridge (Tower Pier)"
]

# Metadata for each year
METADATA = {
  2016: (
    "http://pla.co.uk/assets/platidetablesmaster2016lr.pdf", 830, 7000, 1100, (
      "0345" + ".896" +
      "7120" + "3859" +
      "62"
    )
  ),
  2017: (
    "http://pla.co.uk/assets/platidetables2017.pdf", 830, 7000, 1100, (
      "0134" + ".279" +
      "5869" + "0538" +
      "6208" + "3628" +
      "0623" + "9-"
    )
  ),
  2018: (
    "http://pla.co.uk/assets/pla-tide-tables-2018.pdf", 830, 7000, 1100, (
      "0426" + ".138" +
      "5973" + "0962" +
      "8-"
    )
  ),
  2019: (
    "http://pla.co.uk/assets/pla-tide-tables-2019.pdf", 830, 7000, 1100, (
      "016." + "7438" +
      "2598" + "3059" +
      "26-"
    )
  ),
  2020: (
    "http://pla.co.uk/assets/pla-tide-tables-2020.pdf", 830, 7000, 1100, (
      "034." + "8927" +
      "1565" + "3602" +
      "89-"
    )
  ),
  2021: (
    "http://pla.co.uk/assets/platidetables2021webversion.pdf", 830, 7000, 1100, (
      "047." + "1658" +
      "3299" + "8560" +
      "32"
    )
  ),
  2022: (
    "http://pla.co.uk/assets/platidetable2022webversion.pdf",  900, 7200, 1470, (
      "034." + "8956" +
      "1270" + "5221" +
      "3007" + "3628" +
      "8693" + "6006" +
      "9783" + "8539" +
      "3610" + "8655" +
      "3990" + "5962" +
      "6296" + "289-"
    )
  )
}

# Render a datetime as a string
def to_str(dt):
  return datetime.datetime.strftime(dt, "%Y-%m-%dT%H:%MZ")

# Download, extract and analyze the tidal information for a given year
def get_pages(year, phases, locations, num_pages):
  url, xoff, width, even_y, char_map = METADATA[year]
  print(f"{year}:")

  # Phase 1 - download
  if 1 in phases:
    print(f"  Downloading PDF for {year} from {url}...")
    pdf = urllib.request.urlopen(url).read()
    with open(f"{year}.pdf", "wb") as f:
      f.write(pdf)

  # Phase 2 - extract
  if 2 in phases:
    print(f"  Extracting pages:")
    pathlib.Path(str(year)).mkdir(exist_ok=True)
    for page in range(0, num_pages):
      print(f"    Extracting page {page}...")
      png = f"{year}/{page:02d}.png"
      os.system(f"convert -density 1600 -trim {year}.pdf[{39 + page}] -rotate 90 +repage {png}")

  # Phase 3 - analysis
  if 3 in phases:
    print("  Analyzing pages:")
    ocr = tide_ocr.SimpleOCR(str(year), year, xoff, width, even_y, 0, num_pages)
    ocr.do_ocr()
    results = ocr.parse_all(char_map)

    top = dict()
    top["year"] = year
    top["source"] = url
    top["generator"] = "https://github.com/makestuff/tides-ocr"
    top["data"] = []
    for i in locations:
      d = dict()
      d["location"] = LOCATIONS[i]
      l = [{"ts": to_str(dt), "id": id, "h": h, "dst": dst} for dt, dst, id, h in results[i]]
      d["tides"] = l
      top["data"].append(d)

    print(f"  Writing JSON file to {year}.json...")
    file_name = f"{year}.json"
    with open(file_name, "w") as f:
      json.dump(top, f, indent=2)

  # Done!
  print()

# Get a deduplicated list of ints from a spec like 1,3,5-7,9
def get_list(str):
  s = set()
  result = []
  lst = str.split(",")
  for i in lst:
    rng = i.split("-")
    if len(rng) == 1:
      val = int(i)
      if val not in s:
        result.append(val)
        s.add(val)
    elif len(rng) == 2:
      lower = int(rng[0])
      upper = 1 + int(rng[1])
      if lower > upper:
        raise RuntimeError(f"{lower}-{upper} is not a valid range")
      for j in range(lower, upper):
        val = int(j)
        if val not in s:
          result.append(val)
          s.add(val)
    else:
      raise RuntimeError(f"{'-'.join(rng)} is meaningless")
  return result

# Main entry-point
if len(sys.argv) != 5:
  print(f"Synopsis: {sys.argv[0]} <years> <phases> <locations> <num-pages>")
  print(f"\n    e.g {sys.argv[0]} 2016-2022 1-3, 0-6 48")
  print("\n    phases:")
  print("      1: Download PDFs")
  print("      2: Extract PNGs")
  print("      3: Analyze PNGs")
  print("\n    locations:")
  for i in range(len(LOCATIONS)):
    print(f"      {i}: {LOCATIONS[i]}")
  sys.exit(1)

years = get_list(sys.argv[1])
phases = get_list(sys.argv[2])
locations = get_list(sys.argv[3])
num_pages = int(sys.argv[4])

for year in years:
  get_pages(year, phases, locations, num_pages)
