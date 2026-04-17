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
it already has GMP (see section `2.3` below) built-in, but at the time of writing it lacks a robust binding to ICU (see section `2.3` below);<br />
Python was ultimately chosen for its stability and ecosystem

another consideration is Rust, it has a truly native alternative to GMP (instead of binding), also ICU is actively being rewritten to Rust, but the latter still lacks some required features (for this program) at the time of writing

i also lack designer skill to make a beautiful web interface, so i won’t use JavaScript

as the time of writing, i use latest ICU (v78) which supports latest Unicode (v17)

keep external dependencies to a minimum

![](https://libraryofbabel.info/img/hex802.png "Nested Hexagons")

## 2.2. Unicode

the initial goal was to support all Unicode characters (≈159 801 in Unicode v17), however this leads to impractical constraints:
- book content would be in base-159801.
- the corresponding index base would need to exceed this, which is not feasible

so the trick is to perform **romanization (specifically transliteration)** to bring multilingual text into a manageable Latin-based alphabet, *e.g.* `北京` → `běijīng`

the most straightforward library is https://github.com/avian2/unidecode but it strips a lot of diacritics marks, *e.g.* `北京` → `beijing` (too lossy)

Unicode provides a library to deal with characters, including smarter transliteration: ICU (International Components for Unicode)

but the output is not satisfying: some language-specific punctuation / number characters get through and not transliterated to ASCII punctuation / number<br />
also let’s not forget about emoji

after many trial-and-error, i decided the simplest way is: keep punctuation & symbols in latin and remove all emoji<br />
*N.B.*: i think emoji is too over-bloated, kaomoji is much better `(/≧▽≦)/`

so my version of Library of Babel would be books containing combinations of 8959 Latin-based characters

book index is a character string as combinations of a much wider set: 159 613 printable Unicode characters

![](https://libraryofbabel.info/img/anatomiadelcuerpo.jpg "an 1551 engraving “Historia de la composicion del cuerpo humano” by Juan de Amusco Valverde: a human figure has flayed itself to display its musculature")

## 2.3. some math

book content is an integer in base-8959, book index is the same integer but in base-159613, so $1 - \log_{159\ 613}(8959) \approx 0.24$, therefore the index is only 24% shorter than the content, almost similar to @zwyx

the number of (unique) books in the library is now $8\ 959^{1\ 312\ 000}$

the above value would require $\log_{10}\left(8\ 959^{1\ 312\ 000}\right) = 1\ 312\ 000 \times \log_{10}(8959) \approx 5\ 185\ 365$ digits in base-10

5 millions digits is significantly bigger than original concept (3.2 millions order of magnitude bigger), but modern computers can easily crunch billions of digits

*e.g.* Google Chrome’s JavaScript engine allows us to work with numbers of more than 300 millions digits

*e.g.* the General Multi-Precision (GMP) arithmetic program can theoretically process 1.29 billions digits on 32-bit system, and up to 41.37 billions digits on 64-bit system *given enough RAM and time* (finger-cross with my computer)

book content can also be converted to image, each digit is now a pixel, using RGBA color system a pixel can hold 256⁴ values, so we end up with base-256⁴ *i.e.* base 4 294 967 296 (= 2³²)

example: 1 pixel can have value `00 00 00 ff` meaning red=0, green=0, blue=0, alpha=255

so the book content would require $1\ 312\ 000 \times \log_{4\ 294\ 967\ 296}(8959) = 1\ 312\ 000 \times \frac{\log_2(8959)}{32} \approx 538\ 295$ pixels (*i.e.* digits in base-256⁴)

given $\left\lceil{\sqrt{538\ 295}}\right\rceil = 734$ an image with resolution 734×734 px would be enough to hold a book content<br />
there would be at much $734^2 - 538\ 295 = 461$ excess pixels (less than 0.001%)

there’re 640 books per room, so if we can take the integer value of book content in base-10 divide by 640, the quotient will be room id, the remainder can be mapped to the position of the book in that room, *e.g.*:
- `remainder = 0`: 1st wall, 1st shelf, 1st book in shelf
- `remainder = 639`: 4th wall, 5th shelf, 32nd book in shelf

room id will be also encoded to base-159613 like book id

![](https://libraryofbabel.info/img/hexagrams.jpg "permutations of the possible hexagrams from the I Ching")

## 2.3. coding

for better typing support (PEP 749), i opt to use Python 3.14 (latest version at the time of writing)

GMP (GNU Multiple Precision Arithmetic Library) via `gmpy2`: to process numbers with millions of digits<br />
GMP has been developed since 1991 by arithmetic specialists, `gmpy2` is also regularly maintained since 2007

convention: space character is the zero of base-8959, i don’t care about base-159613

ICU (International Components for Unicode) via `pyicu`: is a bit tricky to install for end users<br />
ICU has been developed since 1999 by internationalization specialists, `pyicu` is impressively maintained since 2007 but very poorly documented<br />
newer implementations exist: `icupy` (no pre-built wheels for windows yet) and `icu4py` (all features not yet available)

i don’t reverse book index order (unlike @zwyx’s implementation)

book content can be converted to image on-the-fly, do not pre-computing all possible pixel color values to avoid out-of-memory

both `gmpy2` & `pyicu` rely heavily on C extensions so only CPython implementation is supported, no PyPy for foreseeable future<br />
they also have not yet support free-threading in Python 3.14

i use `zuban` as type checker because of its conformance, see https://htmlpreview.github.io/?https://github.com/python/typing/blob/main/conformance/results/results.html

### 2.3.1. base conversion routine

the most performance critical part is base conversion routine, the rest is pretty basic operations covered by many ready-to-use packages

`gmpy2` (and also `numpy` or Julia) can only do base conversion up to base-62, i need something else for an arbitrary value

a naive implementation would have quadratic complexity $\mathcal{O}(n^2)$ itself (n = digits count) without accounting for the complexity of big integer multiplication / division algorithm<br />
faster routine use a divide-and-conquer strategy to bring down to sub-quadratic $\mathcal{O}(\text{MD}(n) \log n)$ with `MD(n)` the complexity of big integer multiplication / division algorithm<br />
reference: Richard Brent & Paul Zimmermann (2010). *Modern Computer Arithmetic*, chapter 1 *Integer arithmetic*, section 1.7 *Base conversion*

luckily @zwyx also publish the implementation code of base conversion, see: https://zwyx.dev/blog/base-conversions-with-big-numbers-in-javascript

*bonus*: i found a code to do multi-thread base conversion: https://github.com/taylordotfish/fastconv but i didn’t test yet

*N.B.*: to have the best performance, the base should be a power of 2

the base conversion routine in my program cannot be compiled with `numba` because it doesn’t support arbitrary-precision integers see numba/numba#5005 (max integer width is currently limited to 64-bit, *i.e.* number with $\log_{10}(2^{64}) = 64\log_{10}(2) \approx 20$ digits),<br />
but it can be compiled with `cython` (need benchmarking to see if it’s worth the effort)

although all integers are non-negative, no need to specify as unsigned integer

GPU-acceleration possibilities: as the time of writing, there’re very few libraries in active development (also no Python binding):
- https://github.com/NVlabs/CGBN
- https://homepages.laas.fr/mmjoldes/campary/

Julia has built-in support for arbitrary-precision integers which can be directly used in GPU (need more research to verify)

### 2.3.2. code structure

due to a lack of proper knowledge of design patterns, the code is a mess of object-oriented, functional, and procedural programming styles<br />
but i still try to refactor it while still looking for and learning best practices

```
library-babel/
  │
  ├── my_babel_py/
  │    │
  │    ├── core/
  │    │    ├── config.py       constants
  │    │    └── utils.py        romanization & base conversion
  │    │
  │    ├── io/
  │    │    ├── txt.py          import / export TXT file
  │    │    ├── png.py          import / export PNG image
  │    │    └── pdf.py          export PDF document
  │    │
  │    ├── api/
  │    │    ├── book.py         internal representation
  │    │    ├── randomize.py    generate random book
  │    │    └── search.py       search functionalities
  │    │
  │    ├── cli.py              command-line interface
  │    ├── tui.py              terminal user-interface
  │    ├── gui.py              placeholder
  │    └── webui.py            placeholder
  │
  ├── tests/                    unit tests
  ├── assets/                   other files: font, style, etc.
  ├── docs/                     some writings
  ├── tmp/                      temporary files
  ├── .idea/                    PyCharm settings
  └── .vscode/                  VSCode settings
```
