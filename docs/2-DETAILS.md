# 2. technical details of my Python implementation

## 2.1. design principles

the program would be based on https://github.com/zwyx/library-of-babel

the basic principle is still the same: a full book search, *i.e.*:
- input: text query search, output: index of the book containing the text
- input: book index, output: book content that should contain the text we want initially

the program should be able to support multi language input in text search query

book content as a string is basically a integer in base-`X` with `X` the number of (unique) characters that my program can support in input

book index would be then in base-`Y` with `Y` must be much larger than `X` the index can be shorter than the content

for instance only a command-line interface

possible development: convert to image as book cover, save book as pdf, graphical or web interface, *etc.*

initially, i intended to develop this in Julia, a language i’m currently exploring due to its long-term potential ;<br />
it already has GMP (General Multi-Precision) built-in, but at the time of writing it doesn’t have a full-fledged binding to ICU (International Components for Unicode);<br />
i have opted to use Python for this implementation to ensure stability

i also lack design skill to make a beautiful web interface, so i won’t use Javascript

as the time of writing, i use Python v3.13 (penultimate stable version) of which supports Unicode v16

## 2.2. Unicode

initially i want to cover every Unicode characters, as of version 16 has about 154 998 characters, so the book content is a integer in base-154998, but find the base for book index would be impossible because i would have to go beyond 154998

so the trick is to do romanization, specifically transliteration to Latin alphabet, *e.g.* input `北京` become `běijīng`

the most straightforward library is https://github.com/avian2/unidecode but it strips a lot of diacritics marks, *e.g.* input `北京` simply become `beijing`

Unicode provides a library to deal with characters, including better transliteration: ICU (International Components for Unicode)

but the output is not satisfying: some language-specific punctuation / number characters get through and not transliterated to ASCII punctuation / number<br />
also let’s not forget about emoji

after many trial-and-error, i decided the simplest way is: keep punctuation & symbols in all languages but remove all emoji<br />
*N.B.*: i think emoji is too over-bloated, kaomoji is much better `(/≧▽≦)/`

so my version of Library of Babel would be books containing combinations of 8131 Latin characters

book index is a character string as combinations of any printable Unicode characters: 149 625 characters

![an 1551 engraving “Historia de la composicion del cuerpo humano” by Juan de Amusco Valverde: a human figure has flayed itself to display its musculature](https://libraryofbabel.info/img/anatomiadelcuerpo.jpg)

## 2.3. some math

book content is an integer in base-8131, book index is the same integer but in base-149625, so $1 - \log_{149\ 625}(8131) \approx 0.24$, therefore the book-index string is only 24% shorter than the book-content string (almost the same as @zwyx)

the number of (unique) books in the library is now $8\ 131^{1\ 312\ 000}$

the above value would require $\log_{10}(8\ 131^{1\ 312\ 000}) = 1\ 312\ 000 \times \log_{10}(8\ 131) \approx 5\ 130\ 109$ digits in base-10

5 millions digits is much bigger than original concept (3.2 millions order of magnitude bigger), but modern computers can easily crunching billions of digits

*e.g.* Google Chrome’s JavaScript engine allows us to work with numbers of more than 300 millions digits

*e.g.* the General Multi-Precision (GMP) arithmetic program can theoretically process 1.29 billions digits on 32-bit system, and up to 41.37 billions digits on 64-bit system *given enough RAM and time* (finger-cross with my computer)

book content can also be converted to image, each digit is now a pixel, using RGBA color system a pixel can hold 256⁴ values, so we end up with base-256⁴ *i.e.* base 4 294 967 296

example: 1 pixel can have value `00 00 00 ff` meaning red=0, green=0, blue=0, alpha=255

so the book content would require $1\ 312\ 000 \times \log_{4\ 294\ 967\ 296}(8\ 131) \approx 532\ 558$ pixels (*i.e.* digits in base-256⁴)

an image with resolution 730×730 px would be enough to hold a book content (342px too many)

there’re 640 books per room, so if we can take the integer value of book content in base-10 divide by 640, the quotient will be room id, the remainder can be map to the position of the book in that room, *e.g.*:
- `remainder = 0`: 1st wall, 1st shelf, 1st book in shelf
- `remainder = 639`: 4th wall, 5th shelf, 32nd book in shelf

![permutations of the possible hexagrams from the I Ching](https://libraryofbabel.info/img/hexagrams.jpg)

## 2.3. coding

GMP (General Multi-Precision): use `gmpy2` to process numbers with millions of digits

ICU (International Components for Unicode): `pyicu` is a bit tricky to install for end users

`gmpy2` (and also `numpy` or Julia) can only do base conversion up to base-62, i need something else for an arbitrarily value

luckily @zwyx also publish the code to accelerate base conversion for very big number, see: https://zwyx.dev/blog/base-conversions-with-big-numbers-in-javascript

*bonus*: i found a code to do multi-thread base conversion: https://github.com/taylordotfish/fastconv but i didn’t test yet

*N.B.*: to have the best performance, the base should be a power of 2

convention: space character is the zero of base-8131, i don’t care about base-149625

i don’t reverse book index order like in @zwyx ’s original code

book content convert to image on-the-fly to be used as book cover, don’t generate beforehand the list of all possible pixel colors because it could crash python
