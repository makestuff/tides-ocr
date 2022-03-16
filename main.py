#!/usr/bin/env python3
import tide_ocr

ocr = tide_ocr.SimpleOCR("pages", 0, 48)
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

# Let's have a look at the data for London Bridge from page 20
i = 0
for dt, dst, id, h in results[6][583:610]:
  print(f"results[{i:02d}] = ({dt.strftime('%Y-%m-%dT%H:%M')}, {dst}, {id}, {h})")
  i = i + 1
