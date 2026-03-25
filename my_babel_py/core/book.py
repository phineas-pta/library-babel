# -*- coding: utf-8 -*-

"""
book and properties
"""

from pathlib import Path # for typing only
from warnings import warn
from gmpy2 import mpz # for typing only
from .cste import BOOK_INDEX_CHARACTERS, BOOK_CONTENT_CHARACTERS, SHELVES_PER_WALL, BOOKS_PER_SHELF, BOOKS_PER_ROOM
from .utils import str2int, int2str


class Book:

	def __init__(self, raw_int: mpz = None, index: str = None, content: str = None) -> None:
		if raw_int is not None and index is None and content is None:
			self._raw_int = raw_int
		elif raw_int is None and index is not None and content is None:
			self._raw_int = str2int(index, BOOK_INDEX_CHARACTERS)
		elif raw_int is None and index is None and content is not None:
			self._raw_int = str2int(content, BOOK_CONTENT_CHARACTERS)
		else:
			raise ValueError("provide exactly one of raw_int, index or content")
		# index and content generated lazily when requested, because they are strings so take more memory than the raw integer
		# also i could use raw integer to compute various things later if needed

	@property
	def index(self) -> str:
		"""return book index = integer in base-149625"""
		return int2str(self._raw_int, BOOK_INDEX_CHARACTERS)

	@property
	def content(self) -> str:
		"""return book content = integer in base-8175"""
		return int2str(self._raw_int, BOOK_CONTENT_CHARACTERS)

	def __repr__(self) -> str:
		"""for debugging only"""
		return f"save book to text file to read more, last 5 digits of book id: {self._raw_int % 10**5}"

	def __str__(self) -> str:
		# TODO: need better info
		return f"save book to text file to read more, last 5 digits of book id: {self._raw_int % 10**5}"


###############################################################################
# decorator to transform "save 1 book" function into "save many books"

def save_multiple_books(save1book_func):
	def wrapper(books: list[Book], filepath: Path) -> None:
		if len(books) == 1:
			save1book_func(books[0], filepath)
		else:
			warn("multiple books found, files name will be auto-incremented")
			filename = filepath.stem
			for i, book in enumerate(books):
				new_name = filepath.with_stem(f"{filename}-{i}")
				save1book_func(book, new_name)
	return wrapper
# this function cannot be in file `utils.py` to avoid circular import
