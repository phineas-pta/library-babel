#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase, main, skipUnless
from pathlib import Path
from tempfile import TemporaryDirectory # use temp dir to avoid race condition problem with temp file
from urbabel.core.config import CAPABILITIES
from urbabel.core.utils import transliterate
from urbabel.api.book import Book

if CAPABILITIES["png"]:
	from urbabel.io import read_png


@skipUnless(CAPABILITIES["png"], "no image capability")
class Test_Image_IO(TestCase):
	"""Test the image input / output functions"""
	_input: str
	_output: str
	_tempdir: TemporaryDirectory

	@classmethod
	def setUpClass(cls):
		text = transliterate("\n".join(
			f.read_text(encoding="utf-8")
			for f in Path("docs").glob("*.md")
		)) # also work with text padded with whitespace
		cls._input = Book.zero_pad(text)
		book = Book.from_content(cls._input)
		cls._tempdir = TemporaryDirectory()
		tmp_file = Path(cls._tempdir.name) / "tmp.png"
		book.save_png(tmp_file)
		cls._output = read_png(tmp_file).content

	@classmethod
	def tearDownClass(cls):
		cls._tempdir.cleanup()

	def test_book_position_IO(self):
		self.assertEqual(self._output, self._input, "book content should be kept as-is")


if __name__ == "__main__":
	main()
