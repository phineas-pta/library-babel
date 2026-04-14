#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase, main
from string import ascii_letters, digits, punctuation
from my_babel_py.core.utils import transliterate
# TODO: more exhaustive edge cases
# the categories here aren’t exactly as Unicode categories


class Test_Letters_categories(TestCase):
	"""Test the transliteration of letters (Latin and non-Latin) and also digits"""

	def test_digits(self):
		self.assertEqual(
			transliterate(digits), digits,
			"digits should be kept as-is"
		)

	def test_ascii_letters(self):
		self.assertEqual(
			transliterate(ascii_letters), ascii_letters,
			"ASCII letters should be kept as-is"
		)

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


class Test_nonLetters_categories(TestCase):
	"""Test the transliteration of symbols, punctuation and separators"""

	def test_symbols_and_punctuation(self):
		self.assertEqual(
			transliterate(punctuation), punctuation,
			"symbols and punctuation should be kept as-is"
		)

	def test_separators(self):
		self.assertEqual(
			transliterate("\u0009\u000A\u000D\u0020\u2028\u2029"), chr(32)*6,
			"separators (also TAB, CR, LF) should be replaced by whitespace"
		) # ATTENTION: horizontal tabulation / line feed / carriage return are considered control characters not separators


class Test_removed_categories(TestCase):
	"""Test the transliteration of marks, other characters and emoji"""

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


if __name__ == "__main__":
	main()
