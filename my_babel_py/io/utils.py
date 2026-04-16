# -*- coding: utf-8 -*-

"""
book and properties
"""

from typing import TYPE_CHECKING
from warnings import warn

from ..api.book import Book

if TYPE_CHECKING:
	from collections.abc import Callable
	from pathlib import Path


# decorator to transform "save 1 book" function into "save many books"
def save_multiple_books(save1book_func: Callable) -> Callable:
	def wrapper(books: Book | list[Book] | tuple[Book, ...], filepath: Path, **kwargs) -> None:
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
