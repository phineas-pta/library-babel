#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from my_babel_py.core.char import BOOK_INDEX_CHARACTERS, BOOK_CONTENT_CHARACTERS
from my_babel_py.core.base import str2int, int2str
from my_babel_py.core.translit import transliterate

print("Hello world!")
print(transliterate("Café Αλφτ	άλογος ,,,..:+=- 165 <a>fee</a> 𐄇 $$ 師利言:\n以而瑞,神通相。  ɐɑɒɓɖɗ ᴀᴁᴂᴆᴇᴈᴉ  सेनगुप्त  ᶀᶁᶂᶃᶄ   ₀₁₂₅₆ ⅀⅁⅂⅃⅄ⅅ ⅠⅡⅣⅤⅥ  ﬀﬁﬃﬄ ＠ＡＤＥ"))
