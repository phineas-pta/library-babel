#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase, main
from string import digits, ascii_uppercase, ascii_lowercase, punctuation
from gmpy2 import mpz
from my_babel_py.core.utils import str2int, int2str


class Test_Base_Conversion(TestCase):
	"""Test the base conversion functions `str2int` and `int2str` against `gmpy2`’s built-in base conversion methods."""

	@classmethod
	def setUpClass(cls):
		# `gmpy2` (and `numpy`) can only convert up to base-62
		cls.ALPHABET_base62 = digits + ascii_uppercase + ascii_lowercase # `string.ascii_letters` doesn’t have the same order as `gmpy2`
		cls.RADIX = len(cls.ALPHABET_base62)

	def test_integer_to_string(self):
		TEST_INTs = [
			mpz(67854)**15 - 10,
			mpz(115792089237316195423570985008687907853269984665640564039457584),
			mpz(62)**100 * 256,
			mpz(103147789615402524662804907510279354159900773934860106838120923694590497907642),
			mpz(56789)**43,
		]
		for i in TEST_INTs:
			with self.subTest(num=i):
				self.assertEqual(int2str(i, self.ALPHABET_base62), i.digits(self.RADIX))

	def test_string_to_integer(self):
		TEST_STRs = [
			"5zq4MmqQtfWSswO3zjEK3YKWmUaQ5dmzn2KLwTxnK",
			"DFm4dZo3q6P3MRueTINxmxHaFJagMgRrTEG",
			"48" + "0"*100,
			"s4kFiluFiQ6u38zFtPAhZct63V10dtO9t3thYHCKFpa",
			"1GBDKih5uHQUEK6WSysXRzCX6PWvOFRljqGqfLoxOTyY31pd32rvLQoNTmaWGqGadiHMOQ8839b7jEIgliIyj7y8Pmxg9SpVVIE2lW6gsOAL4qcmoH7",
		]
		for s in TEST_STRs:
			with self.subTest(str=s):
				self.assertEqual(str2int(s, self.ALPHABET_base62), mpz(s, self.RADIX))


class Test_Inconvertible(TestCase):

	def test_out_of_range(self):
		self.assertRaises(ValueError, str2int, text=punctuation, alphabet=digits)

	def test_not_integer(self):
		self.assertRaises(ValueError, int2str, value=0.5, alphabet=digits)


if __name__ == "__main__":
	main()
