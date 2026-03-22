# -*- coding: utf-8 -*-

"""
some constants used in the project
"""

from sys import maxunicode
from icu import UnicodeSet

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

"""
list of all characters to be used in book content,
basically Unicode Latin script except not-printable characters
"""
_tmp0 = [ZERO_CHAR] # space character as 1st character because it is removed in the filter below
_tmp1 = UnicodeSet("[[[:sc=Latin:][:sc=Common:]]&[:Emoji=No:]&[^[:gc=Mark:][:gc=Separator:][:gc=Other:]]]")
for char in _tmp1:
	if char.isprintable():
		_tmp0.append(char)
BOOK_CONTENT_CHARACTERS = tuple(_tmp0)


"""
list of all characters to be used in book index,
basically any printable characters
"""
_tmp2 = []
for code_point in range(maxunicode + 1):
	char = chr(code_point)
	if char.isprintable():
		_tmp2.append(char)
BOOK_INDEX_CHARACTERS = tuple(_tmp2)

assert set(BOOK_CONTENT_CHARACTERS) - set(BOOK_INDEX_CHARACTERS) == set(), "BOOK_CONTENT_CHARACTERS should be a subset of BOOK_INDEX_CHARACTERS"

# assert len(BOOK_CONTENT_CHARACTERS) == 8131, "BOOK_CONTENT_CHARACTERS should contain exactly 8131 characters"
# assert len(BOOK_INDEX_CHARACTERS) == 149625, "BOOK_INDEX_CHARACTERS should contain exactly 149625 characters"
## these numbers can change when Unicode is updated, so we won’t assert it for now

del _tmp0, _tmp1, _tmp2 # clean up temporary variables
