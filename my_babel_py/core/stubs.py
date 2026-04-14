# -*- coding: utf-8 -*-

from dataclasses import dataclass
from gmpy2 import mpz

type Str = str | tuple[str, ...] | list[str]
type Int = int | mpz

@dataclass(frozen=True, slots=True, kw_only=True, repr=False)
class BookPosition:
	book_in_shelf: Int
	shelf_id: Int
	wall_id: Int
	room_id: Int
# dataclass should be better than dict, see https://medium.com/prodigy-engineering/python-from-dictionaries-to-data-classes-b1698a366e6d
