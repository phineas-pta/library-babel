# 1. my discovery journey of Library of Babel

## 1.1. Origin

“The Library of Babel” (Spanish: “La biblioteca de Babel”) is a short story by Argentine author and librarian Jorge Luis Borges (1899–1986), see: https://en.wikipedia.org/wiki/The_Library_of_Babel

![photograph of Borges from 1951](https://libraryofbabel.info/img/borges2.jpg)

An infinite library contains books containing every possible ordering of every character / glyph / grapheme

Though the vast majority of the books in this universe are pure gibberish, the laws of probability dictate that the library also must contain, somewhere, every coherent book ever written, or that might ever be written, and every possible permutation or slightly erroneous version of every one of those books.

I got introduced to that work by in 2021 a friend who was a Portuguese psychiatric nurse. This concept is both beautiful and overwhelming, **in contrast to the incomprehensibility and helplessness in Howard Phillips Lovecraft’s cosmic horror**. Now in 2026 i got better math & coding skills to be able to make my own program (slightly LLM-assisted but not vibe coding by any mean)

*bonus*: from a math point-of-view, the precursor to this story is “The Universal Library” (German: “Die Universalbibliothek”) a short story by German science-fiction writer Kurd Laßwitz, it has approximately same order of magnitude

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

![drawing of the library of Babel’s hexagon pattern by R-Chan](https://libraryofbabel.info/img/hexes2.jpg)

there’re $410 \times 40 \times 80 = 1\ 312\ 000$ characters per book, and the number of (unique) books in the library is therefore $29^{1\ 312\ 000}$

the above value would require $\log_{10}(29^{1\ 312\ 000}) = 1\ 312\ 000 \times \log_{10}(29) \approx 1\ 918\ 667$ so almost 2 millions digits in base-10

with the current human capabilities, **it is not possible to generate or store all books physically or digitally**

besides, there’re $4 × 5 × 32 = 640$ books per room, therefore the number of (unique) rooms in the library is $29^{1\ 312\ 000} \div 640 \approx 2.32 \times 10^{1\ 918\ 663}$, only 0.01% less than the number of (unique) books

there’re also $40 × 80 = 3200$ characters per page, and the number of (unique) pages in the library is $29^{3\ 200}$, therefore there’s at LEAST one duplicate for every page, and if my math is correct: in an ideal case each page is duplicated $29^{1\ 312 \ 000} \div 29^{3\ 200} = 29^{1\ 308\ 800}$ times

the value of number of (unique) pages would require $\log_{10}(29^{3\ 200}) = 3\ 200 \times \log_{10}(29) \approx 4\ 680$ digits in base-10

![](https://github.com/tdjsnelling/babel/blob/master/src/public/image/mucha-2.png)

## 1.2. Digital recreations

as stated above, generate and save all books to be retrieved is impossible

since it’s a library, there must be some sort of library classification system, *e.g.* Dewey decimal system

so the clever idea is come up with an identification system / algorithm that can accept any text as input and give the book index as output

the algorithm must also be invertible, *i.e.* given a book index, return the book content that match the text we want

from a math standpoint, that algorithm must be therefore bijective: book content and book index must be 1-to-1 match

so now the book content / index can be generated on-the-fly on-demand

### 1.2.1. using (pseudo) random number generator

the most popular is the website by Jonathan Basile: https://libraryofbabel.info/ there you can also find the technical details and various of Basile’s writings, which are also worth reading

the source code is partially available: https://github.com/librarianofbabel/libraryofbabel.info-algo but very few documentation

other notable recreation is by Tom Snelling: https://libraryofbabel.app/ and source code: https://github.com/tdjsnelling/babel

various Python implementations exist:
- https://github.com/striter-no/TLoB-v2/tree/main/src/LMath
- https://github.com/cakenggt/Library-Of-Pybel/blob/master/library_of_babel.py
- https://github.com/louis-e/LibraryOfBabel-Python/blob/main/main.py

there’re also implementations in many programming languages: Go, Rust, *etc.*

technical read: https://www.reddit.com/r/BabelForum/comments/vph7p3/a_long_dive_into_the_algorithm_some_math_stupid/

![an illustration of the Library of Babel by Erik Desmazieres: vertiginous shelves surround a central chasm, while librarians carry each other piggy-back across wooden planks](https://libraryofbabel.info/img/desmazierescolor.jpg)

#### 1.2.1.1. technical details

the algorithm is usually a LCG (linear congruential generator) because it’s invertible (therefore bijectivity)

the search text is padded to 3200 characters (*i.e.* 1 page) using spaces or random characters

that string is now a number in base-29

page search seem to be easier, because book search involves crunching an enormous number, *cf.* the math above: page search involve computing 5000-digit numbers meanwhile book search is computing 2million-digit numbers

the program take that number in base-29, convert to base-10 (so ~5000 digits), the algorithm take that number and randomly generate another number in the same order of magnitude, the result is the page index

page index is converted to the form `ROOM.WALL.SHELF.BOOK.PAGE` where: `WALL` is an integer 1-4, `SHELF` is an integer 1-5, `BOOK` is an integer 01-32, `PAGE` is an integer 001-410, while `ROOM` can be alphanumeric with nearly unlimited length using a base-32 or base-36 integer

from page index we can basically get book index

the reverse process is obvious: the algorithm takes page index and return the page containing the text we want

**i got lost with advanced math at this point**, just know that it works!

the shortcomings if of course text query length: 3200 characters max or 1 page ; librarians search books not pages! also the pages got duplicated a lot (*cf.* the math above)

on another hand, as a non-native english speaker, i’ve always wanted Unicode-based solutions for multi-language support, but the math complexity is a significant barrier for me

![from Erik Desmazieres’s illustrations of the library of babel: librarians comb through endlessly receding shelves of books beneath a hexagonal skylight](https://libraryofbabel.info/img/desmazieres5.jpg)

### 1.2.2. no random at all

while wandering on github, i stumble upon by chance on https://babel.zwyx.dev/ and source code: https://github.com/zwyx/library-of-babel

it’s a completely different approach without any randomness: every book every page are sequentially ordered, *i.e.*
- the content of the 1st book in the library (index `0`) is simply 1 312 000 space characters
- the 2nd book (index `1`) is simply the letter `a` which would be placed on the last page of the book, on the last line, at the end of the line. Every other characters before (1,311,999 of them, all the way to the beginning of the book) would be spaces
- book index `2` is the same but wth letter `b`
- *etc.*
- book index `28`, 1 311 999 spaces followed by `z`
- book index `29`, 1 311 998 spaces followed by `a` and a space,
- book index `30`, 1 311 998 spaces followed by `aa`
- *etc.*

i cannot explain it better, just see the details on https://babel.zwyx.dev/?about

the author can actually do a full book search instead of page search

the book content is a base-29 integer with 1 312 000 digits, and the book index is simply the same integer converted to base-94 (94 because of 95 printable characters in the first ASCII code page excluding the space)

the advantage of base-94 is the book index is a string that 49% shorter than the string of that integer in base-10: $1 - \log_{94}(10) \approx 0.49$<br />
but comparing to the the string of book content in base-29: only 26% shorter $1 - \log_{94}(29) \approx 0.26$

the author goes even further with convert that integer to image, basically base-256⁴: a digit is now a pixel in the RGBA color system

**the math is so much simpler that i could write my own program and then add multi-language support**

see [DETAILS](2-DETAILS.md) for technical details about my program

### 1.3. go beyond text

i also found some versions of Library of Babel for image and music with the same philosophy behind; very worth exploring in the future if i have time

![Archimboldi’s Librarian, a trompe-l’œil painting of a human form composed of books](https://libraryofbabel.info/img/bookman2.jpg)
