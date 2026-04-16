# -*- coding: utf-8 -*-

"""
book and properties
"""

from functools import cached_property
from dataclasses import dataclass
from typing import Self, TYPE_CHECKING
from warnings import warn

from ..core import config, utils
from ..io import txt

if TYPE_CHECKING:
	from collections.abc import Generator
	from pathlib import Path
if config.CAPABILITIES["png"]:
	from ..io import png
if config.CAPABILITIES["pdf"]:
	from ..io import pdf


@dataclass(frozen=True, slots=True, kw_only=True, repr=False)
class BookPosition:
	book_in_shelf: utils.Int
	shelf_id: utils.Int
	wall_id: utils.Int
	room_id: utils.Int
# dataclass should be better than dict, see https://medium.com/prodigy-engineering/python-from-dictionaries-to-data-classes-b1698a366e6d


class Book:

	def __init__(self, raw_int: utils.Int) -> None:
		# use multiple constructors pattern to create book from content/position/index, see https://stackoverflow.com/q/682504/10805680
		self._raw_int = raw_int
		# content/position/index will be lazily generated when requested, because they are strings so take more memory than the raw integer
		# also i could use raw integer to compute various things later if needed

	@property
	def raw_int(self) -> utils.Int:
		return self._raw_int

	@staticmethod
	def zero_pad(s: str) -> str:
		if len(s) > config.CHARS_PER_BOOK:
			raise ValueError(f"content is longer than {config.CHARS_PER_BOOK} characters")
		elif len(s) < config.CHARS_PER_BOOK:
			warn(f"content is shorter than {config.CHARS_PER_BOOK} characters, right-justify with whitespaces")
			return s.rjust(config.CHARS_PER_BOOK, config.ZERO_CHAR)
		else:
			return s

	@classmethod
	def from_content(cls, content: str) -> Self:
		s = cls.zero_pad(content)
		return cls(utils.str2int(s, config.BOOK_CONTENT_CHARACTERS))

	@cached_property # avoid repeatedly re-computing in case save to multiple formats
	def content(self) -> str:
		s = utils.int2str(self._raw_int, config.BOOK_CONTENT_CHARACTERS)
		return self.zero_pad(s)

	def get_lines(self) -> Generator[str | int, None, None]:
		"""yield page number and line content"""
		tmp = self.content
		for i in range(0, len(tmp), config.CHARS_PER_LINE):
			if i % config.CHARS_PER_PAGE == 0:
				yield i // config.CHARS_PER_LINE
			yield tmp[i : i+config.CHARS_PER_LINE]

	@classmethod
	def from_position(cls, *, book_in_shelf: utils.Int, shelf_id: utils.Int, wall_id: utils.Int, room_id: utils.Int) -> Self:
		return cls(
			room_id * config.BOOKS_PER_ROOM
			+ config.BOOKS_PER_SHELF * (config.SHELVES_PER_WALL * wall_id + shelf_id)
			+ book_in_shelf
		)

	@property
	def position(self) -> BookPosition:
		"""find the room and position of the book in the room (zero-based index)"""
		# example book content / book index in base-10 is 5342526, then:
		# divmod(5342526, 640) => room_id=8347, remainder=446
		# divmod(446, 32)      => remainder=13, book_in_shelf=30
		# divmod(13, 5)        => wall_id=2, shelf_id=3

		room_id, remainder = divmod(self._raw_int, config.BOOKS_PER_ROOM)  # remainder is always less than BOOKS_PER_ROOM
		remainder, book_in_shelf = divmod(remainder, config.BOOKS_PER_SHELF)
		wall_id, shelf_id = divmod(remainder, config.SHELVES_PER_WALL)
		return BookPosition(book_in_shelf=book_in_shelf, shelf_id=shelf_id, wall_id=wall_id, room_id=room_id)

	@classmethod
	def from_index(cls, index: str) -> Self:
		return cls(utils.str2int(index, config.BOOK_INDEX_CHARACTERS))

	@property
	def index(self) -> str:
		return utils.int2str(self._raw_int, config.BOOK_INDEX_CHARACTERS)

	@property
	def pixels(self) -> list[list[int]]:
		"""
		convert to 2d array to be used in image in RGBA mode
		each pixel is a list of 4 colors with values in range (0-255)
		final array is a list of pixels
		"""
		tmp = utils.int2str(self._raw_int, config.BYTE_HEX) # convert to base 256
		if (rem := len(tmp) % config.PIXEL_LENGTH) != 0: # pad with zeros to make the length a multiple of 8
			tmp = "0" * (config.PIXEL_LENGTH - rem) + tmp

		img_array = []
		for i in range(0, len(tmp), config.PIXEL_LENGTH):
			pixel_color = []
			for j in range(0, config.PIXEL_LENGTH, config.COLOR_LENGTH):
				ij = i + j
				color = int(tmp[ij : ij+config.COLOR_LENGTH], base=16) # convert hex to int
				pixel_color.append(color)
			img_array.append(pixel_color)
		return img_array

	def save_txt_content(self, filepath: Path) -> None:
		txt.txt_save_books_content(self, filepath)
		print(f"book content saved to {filepath}")

	def save_txt_position(self, filepath: Path) -> None:
		txt.txt_save_books_position(self, filepath)
		print(f"book position saved to {filepath}")

	def save_png(self, filepath: Path) -> None:
		if not config.CAPABILITIES["png"]:
			warn("no PNG image export capability, output aborted")
		else:
			png.png_save_books_content(self, filepath)
			print(f"book content saved to {filepath}")

	def save_pdf(self, filepath: Path, *, fontpath: Path | None = None) -> None:
		if not config.CAPABILITIES["pdf"]:
			warn("no PDF document export capability, output aborted")
		else:
			pdf.pdf_save_books_content(self, filepath, fontpath=fontpath)
			print(f"book content saved to {filepath}")

	# TODO: better debugging info
	def __repr__(self, digit=5) -> str:
		"""for debugging only"""
		return f"save book to text file to read more, last {digit} digits of book id: {self._raw_int % 10**digit}"
	def __str__(self, digit=5) -> str:
		"""for debugging only"""
		return f"save book to text file to read more, last {digit} digits of book id: {self._raw_int % 10**digit}"
