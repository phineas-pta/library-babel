#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase, main
from pathlib import Path
from my_babel_py.utils import transliterate
from my_babel_py.book import Book


class Test_Book(TestCase):

	@classmethod
	def setUpClass(cls):
		cls.input = transliterate("\n".join(
			f.read_text(encoding="utf-8")
			for f in Path("docs").glob("*.md")
		)) # also work with text padded with whitespace
		cls.output = Book(content=cls.input).content

	def test_book_content(self):
		self.assertEqual(self.output, self.input, "book content should be kept as-is")


if __name__ == "__main__":
	main()
