# -*- coding: utf-8 -*-

"""
some constants used in the project
TODO: investigate whether python unicode is same as icu
"""

from math import ceil, sqrt, log
import platform
from unicodedata import unidata_version as UNIDATA_VERSION
from importlib.util import find_spec
from gmpy2 import mp_version, version as gmpy2_version
from icu import UnicodeSet, Char, ICU_VERSION, UNICODE_VERSION, VERSION as PYICU_VERSION

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
# find all required characters
# prefer ICU functions instead of Python built-in string methods for consistency

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
		[
			[:Block=Basic_Latin:]
			[:Block=Latin_1_Supplement:]
		] &
		[:Emoji=Yes:]
	]
]""") # this string is found after some trial-and-error with set operations
_tmp1 = [ZERO_CHAR] # space character as 1st character because it is removed in the filter above
for char in _tmp0:
	if Char.isprint(char):
		_tmp1.append(char)
BOOK_CONTENT_CHARACTERS = tuple(_tmp1)


# list of all characters to be used in book index, basically any printable characters
# python str.isprintable() is more restrictive, so when writing to file some characters can be missed
_tmp2 = UnicodeSet("""[^[:General_Category=Separator:][:General_Category=Other:]]""") # should remove a lot of unprintable with python
_tmp2.add(ZERO_CHAR) # doesn’t matter whether append or prepend
BOOK_INDEX_CHARACTERS = tuple(char for char in _tmp2 if Char.isprint(char))


_tmp3 = len(BOOK_CONTENT_CHARACTERS)
_tmp4 = len(BOOK_INDEX_CHARACTERS)


###############################################################################
# only for debugging characters sets

# LIST_PROPERTIES = [x for x in dir(icu.UProperty) if not x.startswith("__")]
# def print_unicode_properties(char: str) -> None:
# 	for prop in LIST_PROPERTIES:
# 		prop_int = getattr(icu.UProperty, prop)
# 		value = icu.Char.getIntPropertyValue(char, prop_int)
# 		prop_value = icu.Char.getPropertyValueName(prop_int, value, icu.UPropertyNameChoice.LONG_PROPERTY_NAME)
# 		print(f"{prop}: {prop_value}")

###############################################################################
# for image processing

BYTE = 2**8 # color = 1 byte = 256 values in each channel R, G, B, A
BYTE_HEX = tuple(f"{i:02x}" for i in range(BYTE)) # hex code

MAX_PIXEL_COUNT = ceil(CHARS_PER_BOOK * log(_tmp3, BYTE**4))
BOOK_IMAGE_SIZE = ceil(sqrt(MAX_PIXEL_COUNT))

COLOR_MODE = "RGBA"
ZERO_COLOR = (0,) * len(COLOR_MODE) # black but transparent
COLOR_LENGTH = 2 # 2 hex characters per color
PIXEL_LENGTH = len(COLOR_MODE) * COLOR_LENGTH # 4 colors × 2 hex characters per color = 8 characters per pixel

###############################################################################
# sys info

CAPABILITIES = {
	"png": find_spec("PIL") is not None,
	"pdf": find_spec("fpdf") is not None,
	"cli": True,
	"tui": False,
	"gui": False,
	"webui": False,
}
def _printTF(x: bool) -> str:
	return "YES" if x else "NO"

SYS_INFO = f"""SYSTEM info:
  - Operating system: {platform.system()} {platform.release()}
  - CPU architecture: {platform.machine()}
  - Python: {platform.python_version()} ({platform.python_implementation()})
  - Required packages:
    - gmpy2 {gmpy2_version()} binding of {mp_version()}
    - pyicu {PYICU_VERSION} binding of ICU {ICU_VERSION}
  - Unicode version:
    - in Python: {UNIDATA_VERSION} (NOT being used)
    - in ICU: {UNICODE_VERSION}
  - Export capabilities: text = YES, image = {_printTF(CAPABILITIES["png"])}, pdf = {_printTF(CAPABILITIES["pdf"])}
  - Interface availabilities:
    - command-line interface = {_printTF(CAPABILITIES["cli"])}
    - terminal user-interface = {_printTF(CAPABILITIES["tui"])}
    - graphical user-interface = {_printTF(CAPABILITIES["gui"])}
    - web-based user-interface = {_printTF(CAPABILITIES["webui"])}

LIBRARY OF BABEL info:
  - {_tmp3:,d} unique characters in book content
  - {_tmp4:,d} unique characters in book index
  - {CHARS_PER_LINE} characters per line
  - {LINES_PER_PAGE} lines per page
  - {PAGES_PER_BOOK} pages per book
  - {BOOKS_PER_SHELF} books per shelf
  - {SHELVES_PER_WALL} bookshelves per wall
  - {WALLS_PER_ROOM} walls per room
therefore:
  - {CHARS_PER_PAGE:,d} characters per page
  - {CHARS_PER_BOOK:,d} characters per book
  - {BOOKS_PER_ROOM} books per room
  - {MAX_PIXEL_COUNT:,d} pixels used to hold book content
  - {BOOK_IMAGE_SIZE}×{BOOK_IMAGE_SIZE}px image size"""

MODIFIED_BOURGES_QUOTE = f"By this art you may contemplate the variation of the {_tmp3} letters"

SRC_URL = "Source code: https://github.com/phineas-pta/library-babel"

del _tmp0, _tmp1, _tmp2, _tmp3, _tmp4 # clean up temporary variables
