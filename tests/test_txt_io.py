#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase, main
from pathlib import Path
from tempfile import TemporaryDirectory # use temp dir to avoid race condition problem with temp file
from my_babel_py.utils import transliterate
from my_babel_py.book import Book
from my_babel_py.txt import txt_save_books_position, txt_load_book_position


class Test_Text_IO(TestCase):
	"""Test the text input / output functions"""

	@classmethod
	def setUpClass(cls):
		tmp_str = transliterate("\n".join(
			f.read_text(encoding="utf-8")
			for f in Path("docs").glob("*.md")
		)) # also work with text padded with whitespace
		cls.input = Book(content=tmp_str)
		cls.tempdir = TemporaryDirectory()
		tmp_file = Path(cls.tempdir.name) / "tmp.txt"
		txt_save_books_position(cls.input, tmp_file)
		cls.output = txt_load_book_position(tmp_file)

	@classmethod
	def tearDownClass(cls):
		cls.tempdir.cleanup()

	def test_book_position(self):
		self.assertEqual(self.output.position, self.input.position, "book position should be kept as-is")

	def test_book_content(self):
		self.assertEqual(self.output.content, self.input.content, "book content should be kept as-is")


if __name__ == "__main__":
	main()
