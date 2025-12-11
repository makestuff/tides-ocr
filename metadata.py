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

# Enum to avoid magic numbers
from enum import IntEnum
class Location(IntEnum):
    WALTON_ON_THE_NAZE = 0
    MARGATE            = 1
    SHIVERING_SAND     = 2
    SOUTHEND_ON_SEA    = 3
    TILBURY            = 4
    NORTH_WOOLWICH     = 5
    LONDON_BRIDGE      = 6

# Metadata for each year
METADATA = {
  2016: (
    "http://pla.co.uk/assets/platidetablesmaster2016lr.pdf", 39, False, 830, 7000, 1100, (
      "0345" + ".896" +
      "7124" + "172"
    )
  ),
  2017: (
    "http://pla.co.uk/assets/platidetables2017.pdf", 39, False, 830, 7000, 1100, (
      "0134" + ".279" +
      "5864" + "1267" +
      "-"
    )
  ),
  2018: (
    "http://pla.co.uk/assets/pla-tide-tables-2018.pdf", 39, False, 830, 7000, 1100, (
      "0426" + ".138" +
      "5974" + "172-"
    )
  ),
  2019: (
    "http://pla.co.uk/assets/pla-tide-tables-2019.pdf", 39, False, 830, 7000, 1100, (
      "016." + "7438" +
      "2594" + "172-"
    )
  ),
  2020: (
    "http://pla.co.uk/assets/pla-tide-tables-2020.pdf", 39, False, 830, 7000, 1100, (
      "034." + "8927" +
      "1562" + "147-"
    )
  ),
  2021: (
    "http://pla.co.uk/assets/platidetables2021webversion.pdf", 39, False, 830, 7000, 1100, (
      "047." + "1658" +
      "3291" + "274"
    )
  ),
  2022: (
    "http://pla.co.uk/assets/platidetable2022webversion.pdf", 39, False, 900, 7200, 1470, (
      "034." + "8956" +
      "1275" + "2021" +
      "4073" + "8806" +
      "3600" + "6913" +
      "5393" + "6086" +
      "8599" + "9162" +
      "2962" + "8899" +
      "-"
    )
  ),
  2023: (
    "http://pla.co.uk/assets/platidetable2023webversion.pdf", 39, False, 900, 7200, 1100, (
      "017." + "3689" +
      "2540" + "2984" +
      "3516" + "7354" +
      "72-"
    )
  ),
  2024: (
    "https://pla.co.uk/sites/default/files/2024-02/platidebooklet2024.pdf", 16, True, 900, 7200, 1100, (
      "0283.947156"
    )
  ),
  2025: (
    "https://pla.co.uk/sites/default/files/2024-12/PLA-Tide-Booklet-2025.pdf", 31, False, 900, 7200, 1100, (
      "084." + "1623" +
      "7950" + "5273" +
      "9486" + "1430" +
      "6"
    )
  ),
  2026: (
    "https://pla.co.uk/sites/default/files/2025-12/PLA-Tide-Booklet-2026.pdf", 31, False, 900, 7200, 1100, (
      "0257" + "1.93" +
      "4860" + "2435" +
      "7169" + "8"
    )
  )
}
