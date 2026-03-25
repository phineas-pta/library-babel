# -*- coding: utf-8 -*-

"""
text output as .txt file
"""

from pathlib import Path # for typing only
from ..core.book import Book, save_multiple_books # decorator to transform "save 1 book" function into "save many books"
from ..core.cste import CHARS_PER_LINE, CHARS_PER_PAGE, BOOK_INDEX_CHARACTERS, SHELVES_PER_WALL, BOOKS_PER_SHELF, BOOKS_PER_ROOM
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

	# find the room and position of the book in the room
	room_id, remainder       = divmod(book._raw_int, BOOKS_PER_ROOM) # remainder is always less than BOOKS_PER_ROOM
	remainder, book_in_shelf = divmod(remainder, BOOKS_PER_SHELF)
	wall_id, shelf_id        = divmod(remainder, SHELVES_PER_WALL)
	# example book content / book index in base-10 is 5342526, then:
	# divmod(5342526, 640) => room_id=8347, remainder=446
	# divmod(446, 32)      => remainder=13, book_in_shelf=30
	# divmod(13, 5)        => wall_id=2, shelf_id=3

	tmp = int2str(room_id, BOOK_INDEX_CHARACTERS) # room id will be also encoded to base-149625 like book id
	with filepath.open(mode="w", encoding="utf-8") as f:
		f.write(f"this is book {1+book_in_shelf} in shelf {1+shelf_id} in wall {1+wall_id} in room:\n")
		for i in range(0, len(tmp), CHARS_PER_LINE):
			f.write(tmp[i:i+CHARS_PER_LINE] + "\n")


def txt_load_book_position(filepath: Path) -> Book:
	with filepath.open(mode="r", encoding="utf-8") as f:
		txt = f.read().splitlines() # .readlines() keep line break which isn’t in BOOK_INDEX_CHARACTERS
	tmp0 = txt[0].split(" ")
	book_in_shelf, shelf_id, wall_id = int(tmp0[3]), int(tmp0[6]), int(tmp0[9]) # TODO: find better way
	room_id = str2int("".join(txt[1:]), BOOK_INDEX_CHARACTERS)
	book_id = room_id * BOOKS_PER_ROOM + BOOKS_PER_SHELF * (SHELVES_PER_WALL * wall_id + shelf_id) + book_in_shelf
	return Book(raw_int=book_id)
