# -*- coding: utf-8 -*-

"""
some constants used in the project
"""

from sys import maxunicode as MAXUNICODE
from itertools import product
from math import ceil, sqrt, log
import platform
from unicodedata import unidata_version as UNIDATA_VERSION
from importlib.util import find_spec
from gmpy2 import mp_version, version as gmpy2_version
from icu import UnicodeSet, ICU_VERSION, UNICODE_VERSION, VERSION as PYICU_VERSION

# values fixed by Borges
WALLS_PER_ROOM   = 4
SHELVES_PER_WALL = 5
BOOKS_PER_SHELF  = 32
PAGES_PER_BOOK   = 410
LINES_PER_PAGE   = 40
CHARS_PER_LINE   = 80

# inferred values
CHARS_PER_PAGE = LINES_PER_PAGE * CHARS_PER_LINE # 3200
CHARS_PER_BOOK = CHARS_PER_PAGE * PAGES_PER_BOOK # 1 312 000
BOOKS_PER_ROOM = WALLS_PER_ROOM * SHELVES_PER_WALL * BOOKS_PER_SHELF # 640

ZERO_CHAR = chr(32) # space character representing 0

###############################################################################
#%% find all required characters

# list of all characters to be used in book content, basically Unicode Latin script except not-printable characters
# see definition of transliterator in file utils.py for more explanation
_tmp0 = UnicodeSet("""[
	[
		[
			[:Script=Latin:]
			[:Script=Common:]
		] &
		[:Emoji=No:] &
		[^
			[:General_Category=Mark:]
			[:General_Category=Other:]
			[:General_Category=Separator:]
		]
	]
	[
		[:Emoji_Component=Yes:] -
		[:Emoji_Modifier=Yes:]
	]
]""") # this string is found after some trial-and-error with set operations
_tmp1 = [ZERO_CHAR] # space character as 1st character because it is removed in the filter above
for char in _tmp0:
	if char.isprintable():
		_tmp1.append(char)
BOOK_CONTENT_CHARACTERS = tuple(_tmp1)


# list of all characters to be used in book index, basically any printable characters
_tmp2 = []
for code_point in range(MAXUNICODE + 1):
	char = chr(code_point)
	if char.isprintable():
		_tmp2.append(char)
BOOK_INDEX_CHARACTERS = tuple(_tmp2)


_tmp3 = len(BOOK_CONTENT_CHARACTERS)
_tmp4 = len(BOOK_INDEX_CHARACTERS)

###############################################################################
#%% for image processing

BYTE = 2**8 # color = 1 byte = 256 values in each channel R, G, B, A
BYTE_HEX = tuple("".join(i) for i in product("0123456789abcdef" , repeat=2)) # hex code

MAX_PIXEL_COUNT = ceil(CHARS_PER_BOOK * log(_tmp3, BYTE**4)) # 532 878 px
BOOK_IMAGE_SIZE = ceil(sqrt(MAX_PIXEL_COUNT)) # 730 px

COLOR_MODE = "RGBA"
ZERO_COLOR = (0,) * len(COLOR_MODE) # black but transparent
COLOR_LENGTH = 2 # 2 hex characters per color
PIXEL_LENGTH = len(COLOR_MODE) * COLOR_LENGTH # 4 colors × 2 hex characters per color = 8 characters per pixel

###############################################################################
#%% sys info

SYS_INFO = f"""SYSTEM info:
  - Operating system: {platform.system()} {platform.release()}
  - Architecture: {platform.machine()}
  - Python: {platform.python_implementation()} {platform.python_version()}
  - Required packages:
    - gmpy2 {gmpy2_version()} binding of {mp_version()}
    - pyicu {PYICU_VERSION} binding of ICU {ICU_VERSION}
  - Unicode:
    - in Python: {UNIDATA_VERSION}
    - in ICU: {UNICODE_VERSION}
  - Export capabilities: text = YES, image = {"NO" if find_spec("PIL") is None else "YES"}, pdf = {"NO" if find_spec("fpdf") is None else "YES"}
  - Interface availabilities: 
    - command-line interface = YES
    - terminal user-interface = NO 
    - graphical user-interface = NO
    - web-based user-interface = NO

LIBRARY OF BABEL info:
  - {_tmp3:,d} unique characters in book content
  - {_tmp4:,d} unique characters in book index
  - {CHARS_PER_LINE} characters per line
  - {LINES_PER_PAGE} lines per page
  - {PAGES_PER_BOOK} pages per book
  - {BOOKS_PER_SHELF} books per shelf
  - {SHELVES_PER_WALL} bookshelves per wall
  - {WALLS_PER_ROOM} room
therefore:
  - {CHARS_PER_PAGE:,d} characters per page
  - {CHARS_PER_BOOK:,d} characters per book
  - {BOOKS_PER_ROOM} books per room
  - {BOOK_IMAGE_SIZE}×{BOOK_IMAGE_SIZE}px image size
  - {MAX_PIXEL_COUNT:,d} pixels used to hold book content"""

del _tmp0, _tmp1, _tmp2, _tmp3, _tmp4 # clean up temporary variables
