# -*- coding: utf-8 -*-

"""
TXT output
"""

from pathlib import Path

from ..core import config, utils
from .utils import save_multiple_books # decorator to transform "save 1 book" function into "save many books"
from ..api import book


@save_multiple_books
def txt_save_books_content(self: book.Book, filepath: Path) -> None:
	"""save the content of the book to a txt file"""
	with filepath.open(mode="w", encoding="utf-8") as f:
		for i in self.get_lines():
			if isinstance(i, int): # add an extra newline after each page
				if i > 0: # not the first page
					f.write("\n")
			else:
				f.write(i + "\n")


@save_multiple_books
def txt_save_books_position(self: book.Book, filepath: Path) -> None:
	"""save the positions of the book to a txt file"""
	tmp = self.position # save to a temporary variable to avoid repeatedly re-computing it
	room_id = utils.int2str(tmp.room_id, config.BOOK_INDEX_CHARACTERS) # room id will be also encoded like book id
	with filepath.open(mode="w", encoding="utf-8") as f:
		f.write(f"this is book {1 + tmp.book_in_shelf} in shelf {1 + tmp.shelf_id} in wall {1 + tmp.wall_id} in room:\n")
		for i in range(0, len(room_id), config.CHARS_PER_LINE):
			f.write(room_id[i : i+config.CHARS_PER_LINE] + "\n")


def txt_load_book_position(filepath: Path) -> book.Book:
	txt = filepath.read_text(encoding="utf-8").splitlines() # .readlines() keep line break which isn’t in BOOK_INDEX_CHARACTERS
	tmp0 = txt[0].split(" ")
	return book.Book.from_position(
		book_in_shelf=int(tmp0[3]) - 1,
		shelf_id=int(tmp0[6]) - 1,
		wall_id=int(tmp0[9]) - 1,
		room_id=utils.str2int("".join(txt[1:]), config.BOOK_INDEX_CHARACTERS),
	)
