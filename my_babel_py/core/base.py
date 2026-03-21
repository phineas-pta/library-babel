# -*- coding: utf-8 -*-

"""
base conversion functions
based on https://zwyx.dev/blog/base-conversions-with-big-numbers-in-javascript
"""

from gmpy2 import mpz # more efficient computation of large integers


def str2int(text: str, alphabet: list[str]) -> mpz:
	"""converts a sequence of base-b digits to an integer in base-10, where b is the length of the alphabet"""
	assert len(set(alphabet)) == len(alphabet), "alphabet must not contain duplicate characters"

	base = len(alphabet)
	parts = [
		{"digit": mpz(alphabet.index(part)), "base": mpz(base)}
		for part in text
	]

	if len(parts) == 1:
		return parts[0]["digit"]

	while len(parts) > 2:
		pair_full = False
		new_parts = []
		for i, curr_part in enumerate(parts):
			if not pair_full:
				if i == len(parts) - 1:
					new_parts.append(curr_part)
				else:
					next_part = parts[i + 1]
					new_parts.append({
						"digit": curr_part["digit"] * next_part["base"] + next_part["digit"],
						"base":  curr_part["base"]  * next_part["base"]
					})
					pair_full = True
			else:
				pair_full = False
		parts = new_parts

	return parts[0]["digit"] * parts[1]["base"] + parts[1]["digit"]


def int2str(value: mpz, alphabet: list[str]) -> str:
	"""converts an integer in base-10 to a sequence of base-b digits, where b is the length of the alphabet"""
	assert len(set(alphabet)) == len(alphabet), "alphabet must not contain duplicate characters"

	if value == 0:
		return alphabet[0]

	number_of_bits_in_value = value.bit_length()
	base = len(alphabet)
	divisors = [mpz(base)]

	# Precompute divisors (base^(2^i))
	while (divisors[-1].bit_length() * 2 - 1) <= number_of_bits_in_value:
		divisors.append(divisors[-1] ** 2)

	# str.join() is most efficient, see: https://docs.python.org/3/faq/programming.html#what-is-the-most-efficient-way-to-concatenate-many-strings-together
	result_parts = []

	def divide(dividend: mpz, divisor_index: mpz) -> None:
		divisor = divisors[divisor_index]
		new_dividend, remainder = divmod(dividend, divisor)

		# Note: To build left-to-right efficiently in Python, we process the quotient first, then the remainder, and append to the list
		if divisor_index > 0:
			divide(new_dividend, divisor_index - 1)
			divide(remainder,    divisor_index - 1)
		else:
			result_parts.append(alphabet[new_dividend])
			result_parts.append(alphabet[remainder])

	divide(value, len(divisors) - 1)

	result = "".join(result_parts).lstrip(alphabet[0]) # remove leading zeros
	return result if result != "" else alphabet[0]
