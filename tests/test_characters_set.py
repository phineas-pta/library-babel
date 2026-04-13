#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase, main, skipUnless
from icu import UNICODE_VERSION
from my_babel_py.config import BOOK_CONTENT_CHARACTERS, BOOK_INDEX_CHARACTERS, BOOK_RANDOM_CHARACTERS

_EXPECTED_VALUES = { # these values come from a specific github actions to count characters
	"17.0": {"content": 8959, "index": 159613}, # ICU v78.x
	"16.0": {"content": 8891, "index": 154810}, # ICU v76.x → v77.x
	"15.1": {"content": 8145, "index": 149625}, # ICU v74.x → v75.x
	"15.0": {"content": 8140, "index": 148998}, # ICU v72.x → v73.x
	"14.0": {"content": 8105, "index": 144516}, # ICU v70.x → v71.x
	"13.0": {"content": 7876, "index": 143680}, # ICU v66.x → v69.x
	"12.1": {"content": 7642, "index": 137750}, # ICU v64.x → v65.x
	"11.0": {"content": 7474, "index": 137204}, # ICU v62.x → v63.x
	"10.0": {"content": 7311, "index": 136521}, # ICU v60.x → v61.x
}
_CHECK_ICU_VERSION = min(_EXPECTED_VALUES.keys()) <= UNICODE_VERSION <= max(_EXPECTED_VALUES.keys())


class Test_Subset(TestCase):

	def test_subset_index(self):
		self.assertEqual(
			set(BOOK_CONTENT_CHARACTERS) - set(BOOK_INDEX_CHARACTERS), set(),
			"BOOK_CONTENT_CHARACTERS should be a subset of BOOK_INDEX_CHARACTERS"
		)

	def test_subset_content(self):
		self.assertEqual(
			set(BOOK_RANDOM_CHARACTERS) - set(BOOK_CONTENT_CHARACTERS), set(),
			"BOOK_RANDOM_CHARACTERS should be a subset of BOOK_CONTENT_CHARACTERS"
		)


class Test_bookContent_charactersSet(TestCase):
	"""Test the integrity of the character set used for book content, ensuring it contains the expected number of unique characters and no duplicates."""

	@skipUnless(_CHECK_ICU_VERSION, "only for ICU ≥ 60")
	def test_length_content(self):
		expected_value = _EXPECTED_VALUES[UNICODE_VERSION]["content"]
		self.assertEqual(
			len(BOOK_CONTENT_CHARACTERS), expected_value,
			f"BOOK_CONTENT_CHARACTERS should contain exactly {expected_value} characters"
		)

	def test_duplicate_content_characters(self):
		self.assertEqual(
			len(BOOK_CONTENT_CHARACTERS), len(set(BOOK_CONTENT_CHARACTERS)),
			"BOOK_CONTENT_CHARACTERS should not contain duplicate characters"
		)


class Test_bookIndex_charactersSet(TestCase):
	"""Test the integrity of the character set used for book indexing, ensuring it contains the expected number of unique characters and no duplicates."""

	@skipUnless(_CHECK_ICU_VERSION, "only for ICU ≥ 60")
	def test_length_index(self):
		expected_value = _EXPECTED_VALUES[UNICODE_VERSION]["index"]
		self.assertEqual(
			len(BOOK_INDEX_CHARACTERS), expected_value,
			f"BOOK_INDEX_CHARACTERS should contain exactly {expected_value} characters"
		)

	def test_duplicate_index_characters(self):
		self.assertEqual(
			len(BOOK_INDEX_CHARACTERS), len(set(BOOK_INDEX_CHARACTERS)),
			"BOOK_INDEX_CHARACTERS should not contain duplicate characters"
		)


if __name__ == "__main__":
	main()
