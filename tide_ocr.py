import cv2
import numpy as np
from matplotlib import pyplot as plt
import datetime
import pytz

#YEAR = 2021
#XMARGIN = 800
#WIDTH = 7100
#EVEN_OFFSET = 1100
TARGET_WIDTH = 80
TARGET_HEIGHT = 110

# Some pages may have spurious symbols, which we need to erase first
fixups = {
  "2022/20.png": [
    (5465, 600, 120, 100),
    (6500, 600, 120, 100)
  ]
}

# Before an image can be displayed, it needs to be converted to RGB
def fix_color(image):
    return(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

# Erase the specified rectangle
def erase_region(image, x, y, w, h):
  image[y:y+h, x:x+w] = 255

# Load, crop and fixup the named image
def image_load_crop_fixup(name, x, y, w):
  image = cv2.imread(name)
  cropped = image[y:, x:x+w]
  if name in fixups:
    for x, y, w, h in fixups[name]:
      erase_region(cropped, x, y, w, h)
  return cropped

# The cv2.findContours() operation seems to find "inner" bounding rects sometimes (e.g the "hole" in a digit 6). We need to remove them.
def remove_inners(bboxes):
    n = len(bboxes)
    bad_set = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            (xi,yi,wi,hi) = bboxes[i]
            (xj,yj,wj,hj) = bboxes[j]
            if xj >= xi and xj+wj <= xi+wi and yj >= yi and yj+hj <= yi+hi:
                bad_set.append(j)
    for bad in sorted(bad_set, reverse=True):
        del bboxes[bad]

# Extract columns of symbols
def extract_columns(bboxes, threshold = 300):
  bboxes.sort(key=lambda r: r[0])
  col_list = []
  this_col = [bboxes[0]]
  for i in range(1, len(bboxes)):
    if bboxes[i][0] - bboxes[i-1][0] < threshold:
      # Add to existing column
      this_col.append(bboxes[i])
    else:
      # Add to new column
      remove_inners(this_col)
      col_list.append(this_col)
      this_col = [bboxes[i]]
  remove_inners(this_col)
  col_list.append(this_col)
  return col_list

# Load the given page, crop it and return an array of column bounding-boxes
def load_page(name, x, y, w):
  cropped = image_load_crop_fixup(name, x, y, w)
  gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
  blurred = cv2.GaussianBlur(gray, (5, 5), 0)
  canny = cv2.Canny(blurred, 30, 300)
  (cnts, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  bboxes = [cv2.boundingRect(cnt) for cnt in cnts]
  col_list = extract_columns(bboxes)
  return cropped, col_list

# Pad image to 70x100 and threshold to get 2-bit colour, inverted
def pad_symbol(image, box):
  (x, y, w, h) = box
  digit = image[y : y+h, x : x+w]
  wm1 = wm2 = int((TARGET_WIDTH - w) / 2)
  hm1 = hm2 = int((TARGET_HEIGHT - h) / 2)
  if wm1 + wm2 + w < TARGET_WIDTH:
      wm2 = wm2 + 1
  if hm1 + hm2 + h < TARGET_HEIGHT:
      hm2 = hm2 + 1
  padded = cv2.copyMakeBorder(digit, hm1, hm2, wm1, wm2, cv2.BORDER_CONSTANT, value=[255,255,255])
  gray = cv2.cvtColor(padded, cv2.COLOR_BGR2GRAY)
  (T, thresh_inv) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
  return thresh_inv

# Extract rows of symbols from a given column, with the symbols in each row sorted left-to-right
def extract_rows(bboxes, threshold = 30):
  bboxes.sort(key=lambda r: r[1] + r[3])
  row_list = []
  old_box = bboxes[0]
  this_row = [old_box]
  for i in range(1, len(bboxes)):
    this_box = bboxes[i]
    if (this_box[1] + this_box[3]) - (old_box[1] + old_box[3]) < threshold:
      # Add to existing row
      this_row.append(this_box)
    else:
      # Add to new row
      this_row.sort(key=lambda r: r[0])
      row_list.append(this_row)
      this_row = [this_box]
    old_box = this_box
  this_row.sort(key=lambda r: r[0])
  row_list.append(this_row)
  return row_list

# Display the provided row-list for debugging
def display_rows(image, row_list):
  for row in row_list:
    symbols_per_row = len(row)
    fig, sp = plt.subplots(1, symbols_per_row)
    fig.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    for i in range(symbols_per_row):
      digit = pad_symbol(image, row[i])
      sp[i].axis("off")
      sp[i].imshow(fix_color(digit))
    plt.show()

# The first four symbols are the time, the remainder is the depth
def parse_line(row, chars):
  row_text = "".join([chars[i] for i in row])
  t = row_text[0:4]
  h = float(row_text[4:])
  return t, h

# Convert the four-digit time into a datetime.timedelta
def time_delta(t):
  hours = int(t[0]) * 10 + int(t[1])
  minutes = int(t[2]) * 10 + int(t[3])
  return datetime.timedelta(hours=hours, minutes=minutes)

# Simple OCR for tide tables
class SimpleOCR:

  # Return an integer value representing the symbol
  def identify_symbol(self, symbol):
    for im, ch in self._symbol_map:
      compare = im.copy()
      similarity = int(cv2.bitwise_xor(symbol, compare).sum()/255)
      if similarity < 30:
        return ch
    ch = self._this_char
    self._symbol_map.append((symbol, ch))
    self._this_char = self._this_char + 1
    return ch

  # Return an array of rows, each row an array of ints representing the symbols in that row
  def read_column(self, image, row_list):
    text_list = []
    for row in row_list:
      symbols_per_row = len(row)
      row_text = []
      for i in range(symbols_per_row):
        symbol = pad_symbol(image, row[i])
        row_text.append(self.identify_symbol(symbol))
      text_list.append(row_text)
    return text_list

  # Construct from a given directory of pages (e.g {dir}/{NN}.png)
  def __init__(self, dir, year, xmargin, width, even_offset, start_page = 0, num_pages = 48):
    self._dir = dir
    self._year = year
    self._xmargin = xmargin
    self._width = width
    self._even_offset = even_offset
    self._start_page = start_page
    self._num_pages = num_pages
    self._symbol_map = []
    self._this_char = 0
    self._columns = [[],[],[],[],[],[],[]]

  def do_ocr(self):
    for p in range(self._start_page, self._start_page + self._num_pages):
      y = self._even_offset if p%2==0 else 0
      cropped, col_list = load_page(f"{self._dir}/{p:02}.png", self._xmargin, y, self._width)
      for i in range(len(col_list)):
        row_list = extract_rows(col_list[i])
        self._columns[i].extend(self.read_column(cropped, row_list))
      print(f"    Cumulative analysis of page {p} revealed {len(self._symbol_map)} distinct symbols!")

  # Show all the unique symbols we've seen
  def show_symbols(self):
    blank = np.zeros((110, 80), dtype=np.uint8)
    symbols_per_row = len(self._symbol_map)
    fig, sp = plt.subplots(8, 8, figsize=(20, 20))
    fig.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    for i in range(8):
      for j in range(8):
        idx = i*8+j
        if idx >= len(self._symbol_map):
          sym = blank
        else:
          sym, _ = self._symbol_map[idx]
        sp[i][j].axis("off")
        sp[i][j].imshow(fix_color(sym))
    plt.show()

  # Convert all columns to typed data
  def parse_all(self, chars):
    lnt = pytz.timezone('Europe/London')
    results = [[],[],[],[],[],[],[]]
    for i in range(len(self._columns)):
      rows = self._columns[i]
      num_rows = len(rows)
      day = 1
      date = datetime.datetime(self._year, 1, 1, tzinfo=datetime.timezone.utc)
      t0, h0 = parse_line(rows[0], chars)
      t1, h1 = parse_line(rows[1], chars)
      id = "HW" if h0 > h1 else "LW"  # find out whether h0 is a HW or LW
      dt = date + time_delta(t0)
      dst = bool(dt.astimezone(lnt).dst())
      results[i].append((dt, dst, id, h0))
      for j in range(1, num_rows):
        t1, h1 = parse_line(rows[j], chars)
        if t1 < t0:
          day = day + 1
          date = date + datetime.timedelta(days=1)
        id = "HW" if h1 > h0 else "LW"  # find out whether h1 is a HW or LW
        dt = date + time_delta(t1)
        dst = bool(dt.astimezone(lnt).dst())
        results[i].append((dt, dst, id, h1))
        t0 = t1
        h0 = h1
    return results

  # Display the named image, after cropping and fixups
  def display_cropped(self, name, even):
    y = self._even_offset if even else 0
    cropped = image_load_crop_fixup(f"{self._dir}/{name}", self._xmargin, y, self._width)
    f = plt.figure(figsize=(20, 20))
    plt.imshow(fix_color(cropped))

  # Put it all together: load an image, crop it, and display some rows
  def display_column(self, name, even, col, num_rows=1, first_row=0):
    y = self._even_offset if even else 0
    cropped, col_list = load_page(f"{self._dir}/{name}", self._xmargin, y, self._width)
    row_list = extract_rows(col_list[col])
    row_sublist = row_list[first_row:first_row + num_rows]
    display_rows(cropped, row_sublist)
