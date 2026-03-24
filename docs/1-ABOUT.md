# 1. my exploration through the Library of Babel

## 1.1. origin

“The Library of Babel” (Spanish: “La biblioteca de Babel”) is a short story by Argentine author and librarian Jorge Luis Borges (1899–1986) published in 1941, see: https://en.wikipedia.org/wiki/The_Library_of_Babel

![](https://libraryofbabel.info/img/borges2.jpg "photograph of Borges from 1951")

The Library contains every possible arrangement of a specific set of characters. While most volumes are absolute gibberish, the laws of probability dictate that it must also contain every coherent book ever written, every book that might be written, and every possible variation or erroneous version thereof.

I was introduced to this concept in 2021 by a friend — a Portuguese psychiatric nurse. I found the concept both hauntingly beautiful and overwhelming, standing **in stark contrast to the cosmic horror of Howard Phillips Lovecraft**, where the unknown is often malicious; here, the unknown is simply a byproduct of mathematical totality. Now, in 2026, equipped with stronger mathematical and coding skills, I am building my own program to navigate this void (slightly LLM-assisted but not vibe coding by any mean).

*Historical note*: The mathematical precursor to Borges’ work is “The Universal Library” (German: “Die Universalbibliothek”) a short story by German science-fiction writer Kurd Laßwitz (1848–1910) published in 1904, which explores a similar order of magnitude.

### 1.1.1. some math

- an infinite amount of adjacent hexagonal rooms
- 4 walls of bookshelves per room
- 5 shelves per wall
- 32 books per shelf
- 410 pages per book
- 40 lines per page
- 80 characters per line
- 29 possible characters: 26 lowercase Latin letters, period (full-stop), comma, and space
  - Borges originally used only 22 letters for a total of 25 characters

![](https://libraryofbabel.info/img/hexes2.jpg "drawing of the library of Babel’s hexagon pattern by R-Chan")

there’re $410 \times 40 \times 80 = 1\ 312\ 000$ characters per book, and the number of (unique) books in the library is therefore $29^{1\ 312\ 000}$

the above value would require $\log_{10}\left(29^{1\ 312\ 000}\right) = 1\ 312\ 000 \times \log_{10}(29) \approx 1\ 918\ 667$ so almost 2 millions digits in base-10

with the current human capabilities, **it is not possible to generate or store all books physically or digitally**

each room contains $4 \times 5 \times 32 = 640$ books, so the number of (unique) rooms in the library is $29^{1\ 312\ 000} \div 640 \approx 2.32 \times 10^{1\ 918\ 663}$, only 0.01% less than the number of (unique) books

each page contains $40 \times 80 = 3200$ characters, and the number of (unique) pages in the library is $29^{3\ 200}$, that means there’s at least one duplicate for every page, and, in an ideal case, each page would be duplicated $29^{1\ 312\ 000} \div 29^{3\ 200} = 29^{1\ 308\ 800}$ times

the value of number of (unique) pages would require $\log_{10}\left(29^{3\ 200}\right) = 3\ 200 \times \log_{10}(29) \approx 4\ 680$ digits in base-10

![](https://libraryofbabel.info/img/bookman2.jpg "Archimboldi’s Librarian, a trompe-l’œil painting of a human form composed of books")

## 1.2. Digital recreations

as stated above, generate and save all books to be retrieved is impossible

since it’s a library, there must be some sort of library classification system, *e.g.* Dewey decimal system

so the clever idea is come up with an identification system / algorithm that takes any text as input and produces the corresponding book index as output

the algorithm must also be invertible, *i.e.* given a book index, it must return the content that matches the target text

from a math point-of-view, that algorithm must be **bijective**: book content and book index must correspond 1-to-1

that way, the content and the index can be generated on-the-fly on-demand instead of being stored all at once

the takeaway is **a book is not stored — it is computed**

### 1.2.1. using (pseudo) random number generator

the best-known recreation is Jonathan Basile’s website: https://libraryofbabel.info/ it also includes technical details and some of Basile’s writings, which are worth reading

part of the source code is available: https://github.com/librarianofbabel/libraryofbabel.info-algo although the documentation is limited

another notable recreation is by Tom Snelling: https://libraryofbabel.app/ and source code: https://github.com/tdjsnelling/babel

various Python implementations exist:
- https://github.com/striter-no/TLoB-v2/tree/main/src/LMath
- https://github.com/cakenggt/Library-Of-Pybel/blob/master/library_of_babel.py
- https://github.com/louis-e/LibraryOfBabel-Python/blob/main/main.py

there’re also implementations in many programming languages: Go, Rust, *etc.*

there’s also an implementation of Library of Babel in Kannada (a language spoken in southwestern India) by Sanath Upadhyaya: https://sanathnu.github.io/Akshara-Mantapa/ with source code: https://github.com/sanathNU/Akshara-Mantapa

technical read:
- https://www.reddit.com/r/BabelForum/comments/vph7p3/a_long_dive_into_the_algorithm_some_math_stupid/
- https://github.com/striter-no/Library-of-Babel
- https://sanathnu.github.io/blog/web/Taming-Infinity.html but more focusing on Upadhyaya’s version

![](https://libraryofbabel.info/img/desmazierescolor.jpg "an illustration of the Library of Babel by Erik Desmazieres: vertiginous shelves surround a central chasm, while librarians carry each other piggy-back across wooden planks")

#### 1.2.1.1. technical details

the algorithm is usually based on a linear congruential generator (LCG) because it is invertible, which makes the mapping bijective

the search text is padded to 3200 characters, which corresponds to one page, using spaces or random characters

that string (page content) is then interpreted as a base-29 number (keep this for later), the aim is to find page index from this number

page search is easier than book search because book search requires handling enormous numbers, *cf.* section `1.1.1.` above: page search involves numbers of around 5000 digits, whereas book search deals with numbers of around 2 million digits

let’s call `N` the number of all possible pages, *i.e.* $N = 29^{3\ 200}$, now find a random number `C` co-prime with `N` then find `I` the modular multiplicative inverse to `C`

now the page index is given by: ${\text{page} \atop \text{index}} = (I \times {\text{page} \atop \text{content}}) \mod N$ (convert page content to base-10 beforehand)

page index is converted to the form `ROOM.WALL.SHELF.BOOK.PAGE` where: `WALL` is an integer 1-4, `SHELF` is an integer 1-5, `BOOK` is an integer 01-32, `PAGE` is an integer 001-410, while `ROOM` can be alphanumeric with any length using a base-32 or base-36 integer

the reverse process is straightforward: the algorithm takes the page index and returns the page containing the desired text: ${\text{page} \atop \text{content}} = (C \times {\text{page} \atop \text{index}}) \mod N$

one of the advantage of this approach is that when we change only 1 character in page content, the page index is nothing alike, pretty similar to cryptographic algorithms (lightweight obfuscation but not as secure)

**i got lost with the advanced math at this point**, but the important part is that it works!

the shortcomings if of course text query length: 3200 characters max or 1 page ; librarians search books not pages! also the pages got duplicated a lot (*cf.* section `1.1.1.` above)

on another hand, as a non-native english speaker, i’ve always wanted Unicode-based solutions for multi-language support, but the math complexity is a serious obstacle for me (however, those operations are trivial to implement in any programming language)

![](https://libraryofbabel.info/img/desmazieres5.jpg "from Erik Desmazieres’s illustrations of the library of babel: librarians comb through endlessly receding shelves of books beneath a hexagonal skylight")

### 1.2.2. no random at all

while wandering on github, i stumble upon by chance on https://babel.zwyx.dev/ and source code: https://github.com/zwyx/library-of-babel

it’s a completely different approach without any randomness: every book every page are sequentially ordered, *i.e.*
- the content of the 1st book in the library (index `0`) is simply 1 312 000 space characters
- the 2nd book (index `1`) is simply the letter `a` which would be placed on the last page of the book, on the last line, at the end of the line. Every other characters before (1 311 999 of them, all the way to the beginning of the book) would be spaces
- book index `2` is the same but wth letter `b`
- *etc.*
- book index `28`, 1 311 999 spaces followed by `z`
- book index `29`, 1 311 998 spaces followed by `a` and a space,
- book index `30`, 1 311 998 spaces followed by `aa`
- *etc.*

i cannot explain it better, just see the details on https://babel.zwyx.dev/?about

in this approach, users can actually perform a full book search rather than a page search

the book content is treated as a base-29 integer with 1 312 000 digits, and the book index is simply the same integer converted to base-94 (94 because of 95 printable characters in the first ASCII code page excluding the space)

the advantage of base 94 is that the resulting book index is about 49% shorter than the decimal representation of the same integer: $1 - \log_{94}(10) \approx 0.49$<br />
but compared with the string representation of the book content in base-29, the index is still about 26% shorter $1 - \log_{94}(29) \approx 0.26$

the takeaway is **a book is not stored as text, but as a very large integer**

the author goes even further and converts the integer into an image, effectively using base-256⁴, where each digit becomes a pixel in the RGBA color system

**because the math here is more intuitive, it provides a perfect foundation for my own goal: adding multi-language support**

see [DETAILS](2-DETAILS.md) for technical details about my program

### 1.3. beyond the text

The philosophy of the Library extends beyond text. If every arrangement of characters exists, then every arrangement of pixels and every arrangement of frequencies must also exist

there’re already some implementations of the Library of Babel for images and music, following the same underlying philosophy ; those are definitely worth exploring in the future

![](https://libraryofbabel.info/img/amazingtechnicolordreamgoat.jpg "the amazing technicolor dream goat")
