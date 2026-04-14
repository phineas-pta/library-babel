# -*- coding: utf-8 -*-

"""
find book given a string
"""

from ..core.config import CHARS_PER_BOOK, ZERO_CHAR
from .book import Book
from ..core.utils import transliterate
from .randomize import generate_random_text


def _preprocess(query: str) -> list[str]:
	"""break search text into list of books"""
	txt = transliterate(query)
	if len(txt) < CHARS_PER_BOOK:
		return [txt]
	else:
		return [txt[i:i+CHARS_PER_BOOK] for i in range(0, len(txt), CHARS_PER_BOOK)]


def search_semi_empty_book(query: str) -> list[Book]:
	"""
	if the search text is shorter than the number of characters per book,
	then the beginning of the book will contain the search text, and the rest of the book will be blank (filled with ZERO_CHAR)

	if the search text is longer than the number of characters per book,
	then split the search text into multiple books, and only the last book will be padded with ZERO_CHAR if needed

	RETURN: a tuple of book(s)
	"""
	tmp = _preprocess(query)
	tmp[-1] = tmp[-1].ljust(CHARS_PER_BOOK, ZERO_CHAR) # pad with ZERO_CHAR to reach the required length for a book
	return [Book.from_content(part) for part in tmp]


def search_semi_random_book(query: str) -> list[Book]:
	"""
	if the search text is shorter than the number of characters per book,
	then the beginning of the book will contain the search text, and the rest of the book will be filled with random characters

	if the search text is longer than the number of characters per book,
	then split the search text into multiple books, and only the last book will be padded with random characters if needed

	RETURN: a tuple of book(s)
	"""
	tmp = _preprocess(query)
	if (k := CHARS_PER_BOOK - len(tmp[-1])) > 0: # padded with random characters if needed
		last_char = tmp[-1][-1]
		if last_char != ZERO_CHAR:
			start_char = last_char
		else:
			start_char = ZERO_CHAR
		tmp[-1] += generate_random_text(k, start_char=start_char)
	return [Book.from_content(part) for part in tmp]
