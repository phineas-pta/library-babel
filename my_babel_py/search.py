# -*- coding: utf-8 -*-

"""
find book given a string
"""

from random import choices
from .core.cste import BOOK_CONTENT_CHARACTERS, CHARS_PER_BOOK, ZERO_CHAR
from .core.utils import transliterate, str2int
from .core.book import Book


def search_semi_empty_book(query: str) -> list[Book]:
	"""
	if the search text is shorter than the number of characters per book,
	then the beginning of the book will contain the search text, and the rest of the book will be blank (filled with ZERO_CHAR)

	if the search text is longer than the number of characters per book,
	then split the search text into multiple books, and only the last book will be padded with ZERO_CHAR if needed

	RETURN: a tuple of book(s)
	"""
	txt = transliterate(query)
	if len(txt) < CHARS_PER_BOOK:
		tmp = [txt]
	else:
		tmp = [txt[i:i+CHARS_PER_BOOK] for i in range(0, len(txt), CHARS_PER_BOOK)]
	tmp[-1] = tmp[-1].ljust(CHARS_PER_BOOK, ZERO_CHAR) # pad with ZERO_CHAR to reach the required length for a book
	return [Book(raw_int=str2int(part, BOOK_CONTENT_CHARACTERS)) for part in tmp]


def search_semi_random_book(query: str) -> list[Book]:
	"""
	if the search text is shorter than the number of characters per book,
	then the beginning of the book will contain the search text, and the rest of the book will be filled with random characters

	if the search text is longer than the number of characters per book,
	then split the search text into multiple books, and only the last book will be padded with random characters if needed

	RETURN: a tuple of book(s)
	"""
	txt = transliterate(query)
	if len(txt) < CHARS_PER_BOOK:
		tmp = [txt]
	else:
		tmp = [txt[i:i+CHARS_PER_BOOK] for i in range(0, len(txt), CHARS_PER_BOOK)]
	if (k := CHARS_PER_BOOK - len(tmp[-1])) > 0: # padded with random characters if needed
		tmp[-1] += "".join(choices(BOOK_CONTENT_CHARACTERS, k=k))
	return [Book(raw_int=str2int(part, BOOK_CONTENT_CHARACTERS)) for part in tmp]
