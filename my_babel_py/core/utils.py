# -*- coding: utf-8 -*-

from icu import Transliterator
from gmpy2 import mpz

###############################################################################
# romanization = transliteration to latin alphabet
# references:
# - https://unicode-org.github.io/icu/userguide/transforms/general/
# - https://unicode-org.github.io/icu/userguide/strings/unicodeset.html
# - https://www.unicode.org/reports/tr35/tr35-general.html#Transform_Rules
# - https://www.unicode.org/Public/UCD/latest/ucd/PropertyValueAliases.txt
# - https://www.unicode.org/charts/
# - https://www.unicode.org/reports/tr51/
# - https://www.unicode.org/Public/UCD/latest/ucd/emoji/emoji-data.txt
# - https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=[%3Aemoji%3A]
# - https://util.unicode.org/UnicodeJsps/transform.jsp

# romanization doesn’t remove all non latin characters, need a special filter
_LEFTOVER_FILTER = "[" + "".join([
	"[^[:Script=Latin:][:Script=Common:]]", # neither latin nor common characters
	"[:General_Category=Mark:][:General_Category=Other:]", # [:General_Category=Separator:] will be replaced with white space
	"[[:Emoji=Yes:] - [:Block=Basic_Latin:] - [:Block=Latin_1_Supplement:]]" # keep #*0123456789©® which are considered emoji (‼⁉️™ will be dealt with NFKC)
]) + "]"

_TRANSLITERATOR = Transliterator.createFromRules("random-label", " ".join([
	":: Latin;", # romanization, must use `::` see icu syntax
	":: NFKC;", # combine diacritics and remove ligatures
	"[[:General_Category=Separator:][:General_Category=Control:]] > ' ';", # replace tab, line feed, etc. with normal white space
	# ATTENTION: horizontal tabulation / line feed / carriage return are considered control characters not separators
	f":: {_LEFTOVER_FILTER} Remove;",
]))
# keep duplicated spaces for case of ASCII art
# to collapse multiple spaces into one space: append ":: Null; ' ' {' '} > ;"
# Null splits the rules into 2 “passes”: 1st pass applies above rules, 2nd pass applies below rules

transliterate = _TRANSLITERATOR.transliterate

###############################################################################
# base conversion functions
# based on https://zwyx.dev/blog/base-conversions-with-big-numbers-in-javascript

type TYPE_STR = str | tuple[str] | list[str] # should be `collections.abc.Sequence` but i’m not sure about `bytes` type
type TYPE_INT = int | mpz
# these lines above require Python 3.12

def str2int(text: TYPE_STR, alphabet: TYPE_STR) -> mpz:
	"""converts a sequence of base-b digits to an integer in base-10, where b is the length of the alphabet"""

	base = len(alphabet)
	powers = {v: i for i, v in enumerate(alphabet)}
	try:
		parts = [{"digit": mpz(powers.get(part)), "base": mpz(base)} for part in text]
		# `powers.get(part)` is much more faster than `alphabet.index(part)` when text is very long
	except (TypeError, KeyError, ValueError):
		_tmp = set(part for part in text if part not in alphabet)
		raise ValueError(f"text contains characters not found in alphabet: {_tmp}")

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


def int2str(value: TYPE_INT, alphabet: TYPE_STR) -> str:
	"""converts an integer in base-10 to a sequence of base-b digits, where b is the length of the alphabet"""

	if not isinstance(value, (mpz, int)):
		raise ValueError("not integer value") # there’re some subtleties but i don’t want to deal with them

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

	def divide(dividend: TYPE_INT, divisor_index: TYPE_INT) -> None:
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
