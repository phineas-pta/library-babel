# technical details of my Python implementation

as stated in [ABOUT](ABOUT.md), this program is based on https://github.com/zwyx/library-of-babel basically a Python implementation with limited multi-language support and for now only work in command line

## Unicode

initially i want to have every Unicode characters, as of version 17 has about 159 801 characters, rendering would be a nightmare

so the trick is to romanization, specifically transliteration to Latin alphabet

the most simple library is https://github.com/avian2/unidecode but it strips a lot of diacritics marks

Unicode provides a library to deal with characters, including better transliteration: ICU (International Components for Unicode)

but the output is not satisfying: some language-specific punctuation / number characters get through and not transliterated to ASCII punctuation

after many trial-and-error, i decided the simplest way is just remove punctuation altogether, the transliteration only keeps letters, numbers and space

so my version of Library of Babel would be books containing 1377 Latin characters, see https://en.wikipedia.org/wiki/Latin_script_in_Unicode but remove all punctuation characters

it isn’t perfect as some symbols have meanings but i would need to deep dive into Unicode docs to figure out how to do it better

book index is a character string containing 320 Latin characters, which is the number of characters i can type using U.S. keyboard layout on Windows, see https://en.wikipedia.org/wiki/Alt_code but only CP850 + CP1252

## some math

book content is an integer in base-1377, book index is an integer in base-320, so `log(1377) / log(320) ≈ 1.25`, therefore i only got 25% denser

in fact to get 2× denser i would need to use full unicode range: `log(159801) / log(320) ≈ 2.08`

the number of (unique) books in the library is now <code>320<sup>1 312 000</sup></code>

the above value would require `1 312 000 × log(320) / log(10) ≈ 3 286 726` digits in base-10

3 millions digits is 3× bigger than original concept, but modern computers can easily crunching billions of digits

e.g. the General Multi-Precision (GMP) arithmetic program can theoretically process 1.29 billion digits on 32-bit system, and up to 41.37 billion decimal digits on 64-bit system given enough RAM and time

## coding

accelerate base conversion for very big number, see: https://zwyx.dev/blog/base-conversions-with-big-numbers-in-javascript

*bonus*: multi-thread base conversion: https://github.com/taylordotfish/fastconv

convention: space character is the zero of base-1377, i don’t care about base-320

i don’t reverse book index order like in @zwyx ’s original code
