# -*- coding: utf-8 -*-

"""
book and properties
"""

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

		# find the room and position of the book in the room
		self._room_id, _remainder       = divmod(self._raw_int, BOOKS_PER_ROOM) # remainder is always less than BOOKS_PER_ROOM
		_remainder, self._book_in_shelf = divmod(_remainder, BOOKS_PER_SHELF)
		self._wall_id, self._shelf_id   = divmod(_remainder, SHELVES_PER_WALL)
		# example book content / book index in base-10 is 5342526, then:
		# divmod(5342526, 640) => room_id=8347, remainder=446
		# divmod(446, 32)      => remainder=13, book_in_shelf=30
		# divmod(13, 5)        => wall_id=2, shelf_id=3

	@property
	def index(self) -> str:
		"""return book index = integer in base-320"""
		return int2str(self._raw_int, BOOK_INDEX_CHARACTERS)

	@property
	def content(self) -> str:
		"""return book content = integer in base-1377"""
		return int2str(self._raw_int, BOOK_CONTENT_CHARACTERS)

	def __str__(self) -> str:
		return "\n\t".join([
			"Book(",
			f"index='{self.index[:80]}',",
			f"content='{self.content[:80]}',",
			f"room_id={self.room_id % 10**80},", # last 80 digits of room_id
			f"wall_id={self.wall_id},",
			f"shelf_id={self.shelf_id},",
			f"book_in_shelf={self.book_in_shelf}",
		]) + "\n)\n"

	@property
	def room_id(self) -> mpz:
		return self._room_id

	@property
	def wall_id(self) -> mpz:
		return self._wall_id

	@property
	def shelf_id(self) -> mpz:
		return self._shelf_id

	@property
	def book_in_shelf(self) -> mpz:
		return self._book_in_shelf
