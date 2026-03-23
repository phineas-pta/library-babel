# -*- coding: utf-8 -*-

"""
text output as .txt file
"""

from pathlib import Path # for typing only
from ..core.book import Book # for typing only
from ..core.cste import CHARS_PER_LINE, CHARS_PER_PAGE


def txt_save_book_content(book: Book, filepath: str | Path) -> None:
	"""save the content of the book to a txt file"""
	tmp = book.content # save the content to a temporary variable to avoid repeatedly re-computing it
	with open(filepath, mode="w", encoding="utf-8") as f:
		for i in range(0, len(tmp), CHARS_PER_LINE):
			if i > 0 and i % CHARS_PER_PAGE == 0: # add an extra newline after each page
				f.write("\n")
			f.write(tmp[i:i+CHARS_PER_LINE] + "\n")


def txt_save_book_position(book: Book, filepath: str | Path) -> None:
	"""save the positions of the book to a txt file"""
	tmp = book.room_id # save the content to a temporary variable to avoid repeatedly re-computing it
	with open(filepath, mode="w", encoding="utf-8") as f:
		f.write(f"this is book {1+book.book_in_shelf} in shelf {1+book.shelf_id} in wall {1+book.wall_id} in room:\n")
		for i in range(0, len(tmp), CHARS_PER_LINE):
			f.write(tmp[i:i+CHARS_PER_LINE] + "\n")
