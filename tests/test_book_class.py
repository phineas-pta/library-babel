#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase, main
from pathlib import Path

from urbabel.core.config import ZERO_CHAR, MAX_PIXEL_COUNT, COLOR_MODE
from urbabel.core.utils import transliterate
from urbabel.api.book import Book


class Test_Book(TestCase):
	_text_zero: str
	_text_long: str
	_text_normal: str
	_book_normal: Book

	@classmethod
	def setUpClass(cls):
		cls._text_zero = ZERO_CHAR
		cls._text_long = "a" * 2000000
		cls._text_normal = transliterate("\n".join(
			f.read_text(encoding="utf-8")
			for f in Path("docs").glob("*.md")
		))
		cls._book_normal = Book.from_content(cls._text_normal)

	def test_1st_book(self):
		position0 = Book.from_content(self._text_zero).position
		self.assertEqual(position0.book_in_shelf, 0, "1st book should be the 1st book in shelf")
		self.assertEqual(position0.shelf_id,      0, "1st book should be in the 1st shelf")
		self.assertEqual(position0.wall_id,       0, "1st book should be in the 1st wall")
		self.assertEqual(position0.room_id,       0, "1st book should be in the 1st room")

	def test_content_too_long(self):
		self.assertRaises(ValueError, Book.from_content, self._text_long)

	def test_book_content(self):
		self.assertEqual(
			self._book_normal.content, Book.zero_pad(self._text_normal),
			"book content should be kept as-is"
		)

	def test_book_pixels(self):
		self.assertLessEqual(
			len(self._book_normal.pixels), MAX_PIXEL_COUNT * len(COLOR_MODE),
			"too many more pixels than expected, need to re-do the math"
		)


if __name__ == "__main__":
	main()
