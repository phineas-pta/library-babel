#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase, main, skipUnless
from pathlib import Path
from tempfile import TemporaryDirectory # use temp dir to avoid race condition problem with temp file
from my_babel_py.core.config import CAPABILITIES
from my_babel_py.core.utils import transliterate
from my_babel_py.api.book import Book

if CAPABILITIES["png"]:
	from my_babel_py.io.png import img_load, img_save_books_content


@skipUnless(CAPABILITIES["png"], "no image capability")
class Test_Image_IO(TestCase):
	"""Test the image input / output functions"""

	@classmethod
	def setUpClass(cls):
		text = transliterate("\n".join(
			f.read_text(encoding="utf-8")
			for f in Path("docs").glob("*.md")
		)) # also work with text padded with whitespace
		cls.input = Book.zero_pad(text)
		book = Book.from_content(cls.input)
		cls.tempdir = TemporaryDirectory()
		tmp_file = Path(cls.tempdir.name) / "tmp.png"
		img_save_books_content(book, tmp_file)
		cls.output = img_load(tmp_file).content

	@classmethod
	def tearDownClass(cls):
		cls.tempdir.cleanup()

	def test_book_position_IO(self):
		self.assertEqual(self.output, self.input, "book content should be kept as-is")


if __name__ == "__main__":
	main()
