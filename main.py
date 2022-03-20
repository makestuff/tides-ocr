#!/usr/bin/env python3

# Before running this, as a minimum, you need to run:
#   download_pdfs.sh       # download all the tide table PDFs
#   extract_pages.sh 2022  # extract the 2022 tide tables as hi-res PNG pages
#
import tide_ocr

# The year we're interested in
YEAR = 2022

# Do the OCR
if YEAR < 2022:
  ocr = tide_ocr.SimpleOCR(str(YEAR), YEAR, 830, 7000, 1100, 0, 48)
else:
  ocr = tide_ocr.SimpleOCR(str(YEAR), YEAR, 900, 7200, 1470, 0, 48)
ocr.do_ocr()
results = ocr.parse_all(
  "034." + "8956" +
  "1270" + "5221" +
  "3007" + "3628" +
  "8693" + "6006" +
  "9783" + "8539" +
  "3610" + "8655" +
  "3990" + "5962" +
  "6296" + "289-"
)

# Let's dump a JSON file of the data for London Bridge
import datetime
import json

# Render a datetime as a string
def to_str(dt):
  return datetime.datetime.strftime(dt, "%Y-%m-%dT%H:%MZ")

# Write the data
lb = [{"loc": "London Bridge (Tower Pier)", "year": YEAR}]
lb.extend([{"ts": to_str(dt), "id": id, "h": h, "dst": dst} for dt, dst, id, h in results[6]])
file_name = f"{YEAR}-london-bridge.json"
with open(file_name, "w") as f:
  json.dump(lb, f, indent=2)
print(f"See {file_name}!")
