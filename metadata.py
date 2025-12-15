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

# Metadata columns
class Columns(IntEnum):
    URL        = 0
    BEGIN_PAGE = 1
    FORCE_EVEN = 2
    XOFF       = 3
    WIDTH      = 4
    EVEN_Y     = 5
    CHAR_MAP   = 6

# Metadata for each year
METADATA = {
  2024: (
    "https://pla.co.uk/sites/default/files/2024-02/platidebooklet2024.pdf", 16, True, 900, 7200, 1100, (
      "0283" + ".947" +
      "156"
    )
  ),
  2025: (
    "https://pla.co.uk/sites/default/files/2024-12/PLA-Tide-Booklet-2025.pdf", 31, False, 900, 7200, 1100, (
      "084." + "1623" +
      "7950" + "3986" +
      "4.30" + "6"
    )
  ),
  2026: (
    "https://pla.co.uk/sites/default/files/2025-12/PLA-Tide-Booklet-2026.pdf", 31, False, 900, 7200, 1100, (
      "0257" + "1.93" +
      "4860" + "3698"
    )
  )
}
