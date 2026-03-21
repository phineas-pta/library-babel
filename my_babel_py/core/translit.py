# -*- coding: utf-8 -*-

import icu

_TRANSLITERATOR = icu.Transliterator.createFromRules("random-label", " ".join([
	":: Latin;", # romanization, must use `::` see icu syntax
	":: NFKC;", # combine diacritics and remove ligatures
	# romatization cannot transform all non-latin characters, so we need to manually deal with the leftover:
	"[[:^Latin:]&[:^Decimal_Number:]] > ' ';", # replace with blankspace instead of remove to avoid concatenating words together
	":: Null;", # splits the rules into 2 “passes”: 1st pass applies above rules, 2nd pass applies below rules
	"' ' {' '} > ;", # collapse multiple spaces into one space
]))

transliterate = _TRANSLITERATOR.transliterate

# DRAFT: to keep all punctations: "[[:^Latin:]&[:^Decimal_Number:]&[:^Symbol:]&[:^Punctuation:]]"
# difficulty is to retrieve all unicode characters in that range in python

# references:
# - https://unicode-org.github.io/icu/userguide/transforms/general/
# - https://unicode-org.github.io/icu/userguide/strings/unicodeset.html
# - https://www.unicode.org/reports/tr44/#General_Category_Values
# - https://www.unicode.org/charts/
