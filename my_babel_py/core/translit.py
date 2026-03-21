# -*- coding: utf-8 -*-

import icu

_TRANSLITERATOR = icu.Transliterator.createFromRules("random-label", " ".join([
	":: Latin;", # romanization, must use `::` see icu syntax
	":: NFKC;", # combine diacritics also remove ligatures
	":: [[:^Separator:] & [:^Latin:] & [:^Nd:]] Remove;", # sometimes romatization can produce non-latin characters
	# [:^Latin:] remove too much, must use [:^Separator:] to keep space and [:^Nd:] to keep digits
	"$space = ' '; $space {$space} >;", # collapse multiple spaces into one space
]))

transliterate = _TRANSLITERATOR.transliterate
