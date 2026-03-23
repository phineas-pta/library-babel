# -*- coding: utf-8 -*-

"""
text output as .txt file
"""

from pathlib import Path # for typing only
from ..core.book import Book, save_multiple_books # decorator to transform "save 1 book" function into "save many books"
from ..core.cste import CHARS_PER_LINE, CHARS_PER_PAGE


@save_multiple_books
def txt_save_books_content(book: Book, filepath: Path) -> None:
	"""save the content of the book to a txt file"""
	tmp = book.content # save the content to a temporary variable to avoid repeatedly re-computing it
	with filepath.open(mode="w", encoding="utf-8") as f: # still use `open` for compatibility
		for i in range(0, len(tmp), CHARS_PER_LINE):
			if i > 0 and i % CHARS_PER_PAGE == 0: # add an extra newline after each page
				f.write("\n")
			f.write(tmp[i:i+CHARS_PER_LINE] + "\n")


@save_multiple_books
def txt_save_books_position(book: Book, filepath: Path) -> None:
	"""save the positions of the book to a txt file"""
	tmp = book.room_id # save the content to a temporary variable to avoid repeatedly re-computing it
	with filepath.open(mode="w", encoding="utf-8") as f: # still use `open` for compatibility
		f.write(f"this is book {1+book.book_in_shelf} in shelf {1+book.shelf_id} in wall {1+book.wall_id} in room:\n")
		for i in range(0, len(tmp), CHARS_PER_LINE):
			f.write(tmp[i:i+CHARS_PER_LINE] + "\n")
