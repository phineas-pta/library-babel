# -*- coding: utf-8 -*-

"""
book and properties
"""

from functools import cached_property
from collections.abc import Callable
from pathlib import Path # for typing only
from warnings import warn
from gmpy2 import mpz # for typing only
from .config import BOOK_INDEX_CHARACTERS, BOOK_CONTENT_CHARACTERS, BOOKS_PER_ROOM, BOOKS_PER_SHELF, SHELVES_PER_WALL
from .utils import str2int, int2str


class Book:

	def __init__(self, *, raw_int: mpz | None = None, content: str | None = None, position: dict[str, int | mpz] | None = None, index: str | None = None) -> None:
		if raw_int is not None and content is None and position is None and index is None:
			self._raw_int = raw_int
		elif raw_int is None and content is not None and position is None and index is None:
			self._raw_int = str2int(content, BOOK_CONTENT_CHARACTERS)
		elif raw_int is None and content is None and position is not None and index is None:
			self._raw_int = position["room_id"] * BOOKS_PER_ROOM + BOOKS_PER_SHELF * (SHELVES_PER_WALL * position["wall_id"] + position["shelf_id"]) + position["book_in_shelf"]
		elif raw_int is None and content is None and position is None and index is not None:
			self._raw_int = str2int(index, BOOK_INDEX_CHARACTERS)
		else:
			raise ValueError("provide exactly one of raw_int, index or content")
		# index and content generated lazily when requested, because they are strings so take more memory than the raw integer
		# also i could use raw integer to compute various things later if needed

	@property
	def raw_int(self) -> mpz:
		return self._raw_int

	@cached_property # avoid repeatedly re-computing in case save to multiple formats
	def content(self) -> str:
		return int2str(self._raw_int, BOOK_CONTENT_CHARACTERS)

	@property
	def position(self) -> dict[str, int | mpz]:
		# find the room and position of the book in the room
		room_id, remainder = divmod(self._raw_int, BOOKS_PER_ROOM)  # remainder is always less than BOOKS_PER_ROOM
		remainder, book_in_shelf = divmod(remainder, BOOKS_PER_SHELF)
		wall_id, shelf_id = divmod(remainder, SHELVES_PER_WALL)

		# example book content / book index in base-10 is 5342526, then:
		# divmod(5342526, 640) => room_id=8347, remainder=446
		# divmod(446, 32)      => remainder=13, book_in_shelf=30
		# divmod(13, 5)        => wall_id=2, shelf_id=3

		return {
			"book_in_shelf": book_in_shelf,
			"shelf_id": shelf_id,
			"wall_id": wall_id,
			"room_id": room_id,
		}

	@property
	def index(self) -> str:
		return int2str(self._raw_int, BOOK_INDEX_CHARACTERS)

	def __repr__(self, digit=5) -> str:
		"""for debugging only""" # TODO: need better info
		return f"save book to text file to read more, last {digit} digits of book id: {self._raw_int % 10**digit}"

	def __str__(self, digit=5) -> str:
		"""for debugging only""" # TODO: need better info
		return f"save book to text file to read more, last {digit} digits of book id: {self._raw_int % 10**digit}"


###############################################################################
# decorator to transform "save 1 book" function into "save many books"

def save_multiple_books(save1book_func: Callable) -> Callable:
	def wrapper(books: Book | list[Book] | tuple[Book], filepath: Path, **kwargs) -> None:
		if isinstance(books, Book):
			save1book_func(books, filepath, **kwargs)
		elif len(books) == 1:
			save1book_func(books[0], filepath, **kwargs)
		else:
			warn("multiple books found, files name will be auto-incremented")
			filename = filepath.stem
			for i, book in enumerate(books):
				new_name = filepath.with_stem(f"{filename}-{i}")
				save1book_func(book, new_name, **kwargs)
	return wrapper
# this function cannot be in file `utils.py` to avoid circular import
