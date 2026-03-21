# 2. technical details of my Python implementation

as stated in [ABOUT](1-ABOUT.md), this program is based on https://github.com/zwyx/library-of-babel basically a Python implementation with limited multi-language support and for now only work in command line

## 2.1. Unicode

initially i want to have every Unicode characters, as of version 17 has about 159 801 characters, rendering would be a nightmare

so the trick is to romanization, specifically transliteration to Latin alphabet

the most simple library is https://github.com/avian2/unidecode but it strips a lot of diacritics marks

Unicode provides a library to deal with characters, including better transliteration: ICU (International Components for Unicode)

but the output is not satisfying: some language-specific punctuation / number characters get through and not transliterated to ASCII punctuation / number

after many trial-and-error, i decided the simplest way is just **remove punctuation altogether, the transliteration only keeps letters, numbers and space**

it isn’t perfect as some symbols have meanings but i would need to deep dive into Unicode docs to figure out how to do it better

so my version of Library of Babel would be books containing 1377 Latin characters, see https://en.wikipedia.org/wiki/Latin_script_in_Unicode but remove all punctuation characters

book index is a character string containing 320 Latin characters, which is the number of characters i can type using U.S. keyboard layout on Windows, see https://en.wikipedia.org/wiki/Alt_code but only CP850 + CP1252

## 2.2. some math

book content is an integer in base-1377, book index is the same integer but in base-320, so `1 - log(320) / log(1377) ≈ 0.2`, therefore the book-index string is only 20% shorter than the book-content string

in fact to get 2× denser i would need to use full unicode range: `1 - log(320) / log(159801) ≈ 0.52`

the number of (unique) books in the library is now <code>1377<sup>1 312 000</sup></code>

the above value would require `1 312 000 × log(1377) / log(10) ≈ 4 118 281` digits in base-10

4 millions digits is much bigger than original concept (2 millions order of magnitude bigger), but modern computers can easily crunching billions of digits

e.g. the General Multi-Precision (GMP) arithmetic program can theoretically process 1.29 billions digits on 32-bit system, and up to 41.37 billions digits on 64-bit system given enough RAM and time

book content can also be converted to image, each digit is now a pixel, using RGBA color system a pixel can hold 256<sup>4</sup> values, so we end up with base-256<sup>4</sup> i.e. base 4 294 967 296

example: `00 00 00 ff` means red=0, green=0, blue=0, alpha=255

so the book content would require `1 312 000 × log(1377) / log(4 294 967 296) ≈ 427 520` pixels (i.e. digits in base-256<sup>4</sup>)

an image with resolution 654×654 px would be enough to hold a book content (more exactly 668×640 px)

there’re 640 books per room, so if we can take book content in base-10 divide by 640, the quotient would be room id and the remainder give the order of wall + shelf + book in that room

## 2.3. coding

`gmpy2` (and also `numpy`) can only do base conversion up to base-62, i need something else for an arbitrarily value

luckily @zwyx also publish the code to accelerate base conversion for very big number, see: https://zwyx.dev/blog/base-conversions-with-big-numbers-in-javascript

*bonus*: i found a code to do multi-thread base conversion: https://github.com/taylordotfish/fastconv but i didn’t test yet

convention: space character is the zero of base-1377, i don’t care about base-320

i don’t reverse book index order like in @zwyx ’s original code

book content convert to image on-the-fly to be used as book cover, don’t generate beforehand the list of all possible pixel colors because it could crash python
