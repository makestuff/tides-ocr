#!/usr/bin/env python3

import tide_ocr
from metadata import METADATA, LOCATIONS
import urllib.request
import os
import sys
import pathlib
import datetime
import json

# Render a datetime as a string
def to_str(dt):
  return datetime.datetime.strftime(dt, "%Y-%m-%dT%H:%MZ")

# Download, extract and analyze the tidal information for a given year
def get_pages(year, phases, locations, num_pages):
  url, begin_page, force_even, xoff, width, even_y, char_map = METADATA[year]
  print(f"{year}:")

  # Phase 1 - download
  if 1 in phases:
    print(f"  Downloading PDF for {year} from {url}...")
    req = urllib.request.Request(
      url, 
      data = None, 
      headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
      }
    )
    pdf = urllib.request.urlopen(req).read()
    with open(f"{year}.pdf", "wb") as f:
      f.write(pdf)

  # Phase 2 - extract
  if 2 in phases:
    print(f"  Extracting pages:")
    pathlib.Path(str(year)).mkdir(exist_ok=True)
    for page in range(0, num_pages):
      print(f"    Extracting page {page}...")
      png = f"{year}/{page:02d}.png"
      os.system(f"convert -density 1600 -trim {year}.pdf[{begin_page + page}] -rotate 90 +repage {png}")

  # Phase 3 - analysis
  if 3 in phases:
    print("  Analyzing pages:")
    ocr = tide_ocr.SimpleOCR(str(year), year, xoff, width, even_y, force_even, 0, num_pages)
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
  print(f"\n    e.g {sys.argv[0]} 2025-2026 1-3, 0-6 48")
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
