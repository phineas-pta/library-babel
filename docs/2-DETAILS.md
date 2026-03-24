# 2. technical details of my Python implementation

## 2.1. design principles

the program would be loosely based on https://github.com/zwyx/library-of-babel

no random number generator involved: this version of Library of Babel is strictly ordered

the core concept remains unchanged:
- SEARCH mode: locate a text within the library
  - input: text query search
  - output: index of the book containing the text
- BROWSE mode: reconstruct the text from its location
  - input: book index
  - output: book content that should contain the text we want initially

supports multilingual input for search queries

the program relies on a finite alphabet, each character is treated as a digit in a positional numeral system, *e.g.* if there’re 29 allowed characters, then each text can be interpreted as a base-29 integer

thus:
- book content (as a string) is represented as an integer in base-`X`, where `X` is the number of supported characters
- book index is represented in base-`Y`, where $Y \gg X$, allowing the index to be shorter than the content.

initial version uses a command-line interface (CLI)

possible future improvements may or may not include: convert book content to image, export book as pdf, build a graphical or web interface, *etc.*

despite the popularity of web interfaces, a local implementation ensures high-performance processing of massive integers without server-side overhead or client-side limitation

initially, i intended to develop this in Julia, a language i’m currently exploring due to its long-term potential ;<br />
it already has GMP (General Multi-Precision) built-in, but at the time of writing it lacks a robust binding to ICU (International Components for Unicode);<br />
Python was ultimately chosen for its stability and ecosystem

i also lack designer skill to make a beautiful web interface, so i won’t use Javascript

as the time of writing, i use Python v3.13 (penultimate stable version) of which supports Unicode v16

keep external dependencies to a minimum

![](https://libraryofbabel.info/img/hex802.png "Nested Hexagons")

## 2.2. Unicode

the initial goal was to support all Unicode characters (≈154 998 in Unicode v16), however this leads to impractical constraints:
- book content would be in base-154998.
- the corresponding index base would need to exceed this, which is not feasible

so the trick is to perform **romanization (specifically transliteration)** to bring multilingual text into a manageable Latin-based alphabet, *e.g.* `北京` → `běijīng`

the most straightforward library is https://github.com/avian2/unidecode but it strips a lot of diacritics marks, *e.g.* `北京` → `beijing` (too lossy)

Unicode provides a library to deal with characters, including smarter transliteration: ICU (International Components for Unicode)

but the output is not satisfying: some language-specific punctuation / number characters get through and not transliterated to ASCII punctuation / number<br />
also let’s not forget about emoji

after many trial-and-error, i decided the simplest way is: keep punctuation & symbols in latin and remove all emoji<br />
*N.B.*: i think emoji is too over-bloated, kaomoji is much better `(/≧▽≦)/`

so my version of Library of Babel would be books containing combinations of 8175 Latin-based characters

book index is a character string as combinations of a much wider set: 149 625 printable Unicode characters

![](https://libraryofbabel.info/img/anatomiadelcuerpo.jpg "an 1551 engraving “Historia de la composicion del cuerpo humano” by Juan de Amusco Valverde: a human figure has flayed itself to display its musculature")

## 2.3. some math

book content is an integer in base-8175, book index is the same integer but in base-149625, so $1 - \log_{149\ 625}(8175) \approx 0.24$, therefore the index is only 24% shorter than the content, almost similar to @zwyx

the number of (unique) books in the library is now $8\ 175^{1\ 312\ 000}$

the above value would require $\log_{10}\left(8\ 175^{1\ 312\ 000}\right) = 1\ 312\ 000 \times \log_{10}(8175) \approx 5\ 133\ 184$ digits in base-10

5 millions digits is significantly bigger than original concept (3.2 millions order of magnitude bigger), but modern computers can easily crunching billions of digits

*e.g.* Google Chrome’s JavaScript engine allows us to work with numbers of more than 300 millions digits

*e.g.* the General Multi-Precision (GMP) arithmetic program can theoretically process 1.29 billions digits on 32-bit system, and up to 41.37 billions digits on 64-bit system *given enough RAM and time* (finger-cross with my computer)

book content can also be converted to image, each digit is now a pixel, using RGBA color system a pixel can hold 256⁴ values, so we end up with base-256⁴ *i.e.* base 4 294 967 296 (= 2³²)

example: 1 pixel can have value `00 00 00 ff` meaning red=0, green=0, blue=0, alpha=255

so the book content would require $1\ 312\ 000 \times \log_{4\ 294\ 967\ 296}(8175) \approx 532\ 878$ pixels (*i.e.* digits in base-256⁴)

given $\left\lceil{\sqrt{532\ 878}}\right\rceil = 730$ an image with resolution 730×730 px would be enough to hold a book content<br />
there would be at much $730^2 - 538\ 878 = 22$ excess pixels (less than 0.004%)

there’re 640 books per room, so if we can take the integer value of book content in base-10 divide by 640, the quotient will be room id, the remainder can be map to the position of the book in that room, *e.g.*:
- `remainder = 0`: 1st wall, 1st shelf, 1st book in shelf
- `remainder = 639`: 4th wall, 5th shelf, 32nd book in shelf

room id will be also encoded to base-149625 like book id

![](https://libraryofbabel.info/img/hexagrams.jpg "permutations of the possible hexagrams from the I Ching")

## 2.3. coding

GMP (General Multi-Precision) via `gmpy2`: to process numbers with millions of digits

ICU (International Components for Unicode) via `pyicu`: is a bit tricky to install for end users

`gmpy2` (and also `numpy` or Julia) can only do base conversion up to base-62, i need something else for an arbitrarily value

luckily @zwyx also publish the code to accelerate base conversion for very big number, see: https://zwyx.dev/blog/base-conversions-with-big-numbers-in-javascript

*bonus*: i found a code to do multi-thread base conversion: https://github.com/taylordotfish/fastconv but i didn’t test yet

*N.B.*: to have the best performance, the base should be a power of 2

convention: space character is the zero of base-8175, i don’t care about base-149625

i don’t reverse book index order (unlike @zwyx’s implementation)

although all integers are non negative, no need to specify as unsigned integer

book content can be converted to image on-the-fly, avoid pre-computing all possible pixel values to prevent memory issues
