# -*- coding: utf-8 -*-

"""
randomly fill a book
feature: tweak the probabilities so spaces appear more often (i.e. more word-like)

naive implementation would be just increase the probability of whitespace
better implementation would be a Markov chain

i cannot find any resources concerning Zipf’s law in romanized texts
so the probabilities are far from ideal
"""

from random import random, choice
from icu import UnicodeSet, Char

from ..core import config
from .book import Book


_W_SPACE = 0.15 # in english it’s around 18% but i want longer words

## naive implementation (DO NOT USE because multiple spaces)
# _my_list = abc…xyz
# def _generate_random_text(length: int) -> str:
# 	tmp = len(_my_list) - 1
# 	weights = [_W_SPACE] + [(1 - _W_SPACE) / tmp for _ in range(tmp)]
# 	return "".join(random.choices(_my_list, weights, k=length))


# characters to be used to generate random text (excluding symbols)
# for more: https://en.wikipedia.org/wiki/Latin_script_in_Unicode
_tmp = UnicodeSet("""[
	[
		[:General_Category=Letter:]
		[:General_Category=Number:]
	] &
	[
		[:Block=Basic_Latin:]
		[:Block=Latin_1_Supplement:]
		[:Block=Latin_Extended_A:]
		[:Block=Latin_Extended_Additional:]
		[:Block=Latin_Extended_B:]
		[:Block=Latin_Extended_C:]
	]
]""")
_UPPER, _LOWER, _DIGIT = [], [], []
for char in _tmp:
	if Char.isupper(char):
		_UPPER.append(char)
	elif Char.islower(char):
		_LOWER.append(char)
	elif Char.isdigit(char):
		_DIGIT.append(char)
	else:
		continue
_ALL = _UPPER + _LOWER + _DIGIT
# no whitespace here because it will be dealt differently


def _get_next_char(current_char: str) -> str:
	"""
	realize a random walk following this matrix
	   next┌───────┬─────────┬─────────┬───────┐
	curr   │ space │  upper  │  lower  │ digit │
	┌──────┼───────┼─────────┴─────────┴───────┤
	│space │   0   │              1            │
	│upper │   W   │ (1-W)/2 │ (1-W)/2 │   0   │
	│lower │   W   │    0    │   1-W   │   0   │
	│digit │   W   │    0    │    0    │  1-W  │
	└──────┴───────┴─────────┴─────────┴───────┘
	inspired from https://www.voynich.nu/misc/misc_07.html
	"""
	prob = random()
	if current_char == config.ZERO_CHAR:
		return choice(_ALL)
	elif current_char in _UPPER:
		if prob < _W_SPACE:
			return config.ZERO_CHAR
		elif prob < (1 + _W_SPACE) / 2:
			return choice(_UPPER)
		else:
			return choice(_LOWER)
	elif current_char in _LOWER:
		if prob < _W_SPACE:
			return config.ZERO_CHAR
		else:
			return choice(_LOWER)
	elif current_char in _DIGIT:
		if prob < _W_SPACE:
			return config.ZERO_CHAR
		else:
			return choice(_DIGIT)
	else:
		return config.ZERO_CHAR


def generate_random_text(length: int, *, start_char: str) -> str:
	"""using a very simple Markov chain"""
	res = [start_char] * length
	for i in range(length-1):
		res[i+1] = _get_next_char(res[i])
	return "".join(res)


def pick_random_book() -> Book:
	"""pick a completely random book"""
	return Book.from_content(generate_random_text(config.CHARS_PER_BOOK, start_char=choice(_ALL)))
