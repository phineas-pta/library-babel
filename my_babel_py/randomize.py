# -*- coding: utf-8 -*-

"""
randomly fill a book
feature: tweak the probabilities so spaces appear more often (i.e. more word-like)

naive implementation would be just increase the probability of whitespace
better implementation would be a Markov chain
for more technical read: https://www.voynich.nu/misc/misc_07.html

i cannot find any resources concerning Zipf’s law in romanized texts
so the probabilities are far from ideal
"""

from random import random, choice
from .book import Book
from .config import BOOK_RANDOM_CHARACTERS, CHARS_PER_BOOK, ZERO_CHAR


_W_SPACE = 0.15 # in english it’s around 18% but i want longer words

## naive implementation (DO NOT USE because multiple spaces)
# def _generate_random_text(length: int) -> str:
# 	tmp = len(BOOK_RANDOM_CHARACTERS) - 1
# 	weights = [_W_SPACE] + [(1 - _W_SPACE) / tmp for _ in range(tmp)]
# 	return "".join(random.choices(BOOK_RANDOM_CHARACTERS, weights, k=length))


def generate_random_text(length: int) -> str:
	"""using a very simple Markov chain"""
	current_char = ZERO_CHAR
	res = [current_char]
	while len(res) < length:
		char = choice(BOOK_RANDOM_CHARACTERS)
		if current_char == ZERO_CHAR:
			current_char = char # avoid multiple spaces
		else:
			if random() < _W_SPACE:
				current_char = ZERO_CHAR
			else:
				current_char = char
		res.append(current_char)
	return "".join(res)


def pick_random_book() -> Book:
	"""pick a completely random book"""
	return Book(content=generate_random_text(CHARS_PER_BOOK))
