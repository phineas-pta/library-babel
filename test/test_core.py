#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase, skipUnless, main
from unicodedata import unidata_version as UNIDATA_VERSION
from gmpy2 import mpz
from icu import UNICODE_VERSION
from my_babel_py.core.cste import BOOK_CONTENT_CHARACTERS, BOOK_INDEX_CHARACTERS, BYTE, BYTE_HEX
from my_babel_py.core.utils import transliterate, str2int, int2str


class Test_Characters(TestCase):

	length_index = len(BOOK_INDEX_CHARACTERS)
	length_content = len(BOOK_CONTENT_CHARACTERS)
	set_index = set(BOOK_INDEX_CHARACTERS)
	set_content = set(BOOK_CONTENT_CHARACTERS)

	@skipUnless(UNIDATA_VERSION == "15.1.0", "this number can change on different Python version")
	def test_length_index(self):
		self.assertEqual(
			self.length_index, 149625,
			"BOOK_INDEX_CHARACTERS should contain exactly 149625 characters"
		)

	@skipUnless(UNICODE_VERSION == "17.0", "this number can change on different ICU version")
	def test_length_content(self):
		self.assertEqual(
			self.length_content, 8175,
			"BOOK_CONTENT_CHARACTERS should contain exactly 8175 characters"
		)

	def test_duplicate_index_characters(self):
		self.assertEqual(
			self.length_index, len(self.set_index),
			"BOOK_INDEX_CHARACTERS should not contain duplicate characters"
		)

	def test_duplicate_content_characters(self):
		self.assertEqual(
			self.length_content, len(self.set_content),
			"BOOK_CONTENT_CHARACTERS should not contain duplicate characters"
		)

	def test_subset(self):
		self.assertEqual(
			self.set_content - self.set_index, set(),
			"BOOK_CONTENT_CHARACTERS should be a subset of BOOK_INDEX_CHARACTERS"
		)

	def test_color(self):
		self.assertEqual(
			len(BYTE_HEX), BYTE,
			"BYTE_HEX should contain exactly 256 characters"
		)
		self.assertEqual(
			len(BYTE_HEX), len(set(BYTE_HEX)),
			"BYTE_HEX should not contain duplicate characters"
		)


class Test_Romanization(TestCase): # TODO: more edge cases

	def test_latin_script(self):
		tmp = "tác phẩm “Thư viện Babel” của Borges"
		self.assertEqual(
			transliterate(tmp), tmp,
			"Latin scripts should be kept as-is"
		)

	def test_non_latin_script(self):
		self.assertEqual(
			transliterate("《巴别图书馆》"), "«bā bié tú shū guǎn»",
			"non-Latin scripts should be transliterated"
		)

	def test_right2left_script(self):
		self.assertEqual(
			transliterate("مكتبة بابل"), "mktbẗ bạbl",
			"right-to-left scripts should become left-to-right"
		)

	def test_symbols_and_punctuation(self):
		tmp = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
		self.assertEqual(
			transliterate(tmp), tmp,
			"symbols and punctuation should be kept as-is"
		)

	def test_separators(self):
		self.assertEqual(
			transliterate("\u0009\u000A\u000D\u0020\u2028\u2029"), chr(32)*6,
			"separators should be replaced by whitespace"
		) # ATTENTION: horizontal tabulation / line feed / carriage return are considered control characters not separators

	def test_other(self):
		self.assertEqual(
			transliterate("\u0300\u0304\u0308\u030C\u0378\u0379\uE000\uE004\uE008\uE00C"), "",
			"marks and other characters should be removed"
		) # control characters are replaced by whitespace

	def test_emoji(self):
		self.assertEqual(
			transliterate("😘🤗👻👀🤿⚒️🍭🚲🧻💤🙄"), "",
			"emoji should be removed"
		)


class Test_Base_Conversion(TestCase): # TODO: change hard-coded values

	alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" # base-62
	test_int = mpz(67854)**15 - 10
	test_str = "5zq4MmqQtfWSswO3zjEK3YKWmUaQ5dmzn2KLwTxnK"

	def test_integer_to_string(self):
		self.assertEqual(
			int2str(self.test_int, self.alphabet), self.test_int.digits(62),
			"returned string not matched"
		)

	def test_string_to_integer(self):
		self.assertEqual(
			str2int(self.test_str, self.alphabet), mpz(self.test_str, 62),
			"returned integer not matched"
		)


if __name__ == "__main__":
	main()
