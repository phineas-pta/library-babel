#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase, main
from pathlib import Path
from tempfile import TemporaryDirectory # use temp dir to avoid race condition problem with temp file

from urbabel.core.utils import transliterate
from urbabel.api.book import Book
from urbabel.io import read_txt_position


class Test_Text_IO(TestCase):
	"""Test the text input / output functions"""
	_input: Book
	_output: Book
	_tempdir: TemporaryDirectory

	@classmethod
	def setUpClass(cls):
		tmp_str = transliterate("\n".join(
			f.read_text(encoding="utf-8")
			for f in Path("docs").glob("*.md")
		)) # also work with text padded with whitespace
		cls._input = Book.from_content(tmp_str)
		cls._tempdir = TemporaryDirectory()
		tmp_file = Path(cls._tempdir.name) / "tmp.txt"
		cls._input.save_txt_position(tmp_file)
		cls._output = read_txt_position(tmp_file)

	@classmethod
	def tearDownClass(cls):
		cls._tempdir.cleanup()

	def test_book_position(self):
		self.assertEqual(self._output.position, self._input.position, "book position should be kept as-is")

	def test_book_content(self):
		self.assertEqual(self._output.content, self._input.content, "book content should be kept as-is")


if __name__ == "__main__":
	main()
