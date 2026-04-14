# -*- coding: utf-8 -*-

"""
text output as .txt file
"""

from pathlib import Path # for typing only
from ..api.book import Book, BookPosition, save_multiple_books # decorator to transform "save 1 book" function into "save many books"
from ..core.config import CHARS_PER_LINE, CHARS_PER_PAGE, BOOK_INDEX_CHARACTERS
from ..core.utils import str2int, int2str


@save_multiple_books
def txt_save_books_content(book: Book, filepath: Path) -> None:
	"""save the content of the book to a txt file"""
	tmp = book.content # save the content to a temporary variable to avoid repeatedly re-computing it
	with filepath.open(mode="w", encoding="utf-8") as f:
		for i in range(0, len(tmp), CHARS_PER_LINE):
			if i > 0 and i % CHARS_PER_PAGE == 0: # add an extra newline after each page
				f.write("\n")
			f.write(tmp[i:i+CHARS_PER_LINE] + "\n")


@save_multiple_books
def txt_save_books_position(book: Book, filepath: Path) -> None:
	"""save the positions of the book to a txt file"""
	tmp0 = book.position
	book_in_shelf = tmp0.book_in_shelf
	shelf_id = tmp0.shelf_id
	wall_id = tmp0.wall_id
	room_id = int2str(tmp0.room_id, BOOK_INDEX_CHARACTERS) # room id will be also encoded like book id
	with filepath.open(mode="w", encoding="utf-8") as f:
		f.write(f"this is book {1+book_in_shelf} in shelf {1+shelf_id} in wall {1+wall_id} in room:\n")
		for i in range(0, len(room_id), CHARS_PER_LINE):
			f.write(room_id[i:i+CHARS_PER_LINE] + "\n")


def txt_load_book_position(filepath: Path) -> Book:
	txt = filepath.read_text(encoding="utf-8").splitlines() # .readlines() keep line break which isn’t in BOOK_INDEX_CHARACTERS
	tmp0 = txt[0].split(" ")
	position = BookPosition(
		book_in_shelf=int(tmp0[3]) - 1,
		shelf_id=int(tmp0[6]) - 1,
		wall_id=int(tmp0[9]) - 1,
		room_id=str2int("".join(txt[1:]), BOOK_INDEX_CHARACTERS),
	)
	return Book.from_position(position)
