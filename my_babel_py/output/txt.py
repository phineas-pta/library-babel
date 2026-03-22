# -*- coding: utf-8 -*-

"""
text output as .txt file
"""

from ..core.book import Book # for typing only
from ..core.cste import CHARS_PER_LINE, CHARS_PER_PAGE


def save_book_content(book: Book, filename: str) -> None:
	"""save the content of the book to a txt file"""
	with open(filename, "w", encoding="utf-8") as f:
		tmp = book.content # save the content to a temporary variable to avoid repeatedly re-computing it
		for i in range(0, len(tmp), CHARS_PER_LINE):
			if i > 0 and i % CHARS_PER_PAGE == 0: # add an extra newline after each page
				f.write("\n")
			f.write(tmp[i:i+CHARS_PER_LINE] + "\n")
