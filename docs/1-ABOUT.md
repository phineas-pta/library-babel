# 1. my discovery journey of Library of Babel

## 1.1. Origin

“The Library of Babel” (Spanish: “La biblioteca de Babel”) is a short story by Argentine author and librarian Jorge Luis Borges (1899–1986), see: https://en.wikipedia.org/wiki/The_Library_of_Babel

An infinite library contains books containing every possible ordering of every character / glyph / grapheme

Though the vast majority of the books in this universe are pure gibberish, the laws of probability dictate that the library also must contain, somewhere, every coherent book ever written, or that might ever be written, and every possible permutation or slightly erroneous version of every one of those books.

I got introduced to that work by my Portuguese-nurse friend in 2021. This concept is both beautiful and overwhelming, **in constrast to the incomprehensibility and helplessness in Howard Phillips Lovecraft’s cosmic horror**. Now in 2026 i got better math & coding skills to make my own program (slightly LLM-assisted but not vibe coding by any mean)

*bonus*: from a math point-of-view, the precursor to this story is “The Universal Library” (German: “Die Universalbibliothek”) a short story by German science-fiction writer Kurd Laßwitz, it has approximately same order of magnitude

### 1.1.1. some math

- an infinite amount of adjacent hexagonal rooms
- 4 walls of bookshelves per room
- 5 shelves per bookshelf
- 32 books per shelf
- 410 pages per book
- 40 lines per page
- 80 characters per line
- 29 possible characters: 26 lowercase Latin letters, period (full-stop), comma, and space
  - Borges originally used only 22 letters for a total of 25 characters

there’re `410 × 40 × 80 = 1 312 000` characters per book, and the number of (unique) books in the library is therefore <code>29<sup>1 312 000</sup></code>

the above value would require `1 312 000 × log(29) / log(10) ≈ 1 918 667` so almost 2 millions digits in base-10

with the current human capabilities, **it is not possible to generate and store all books physically nor digitally**

besides, there’re also `4 × 5 × 32 = 640` books per room, therefore the number of (unique) rooms in the library is<code>29<sup>1 312 000</sup> ÷ 640 ≈ 2.32×10<sup>1918663</sup></code>, only 0.01% less than the number of (unique) books

besides, there’re also `40 × 80 = 3200` characters per page, and the number of (unique) pages in the library is <code>29<sup>3200</sup></code>, therefore there’s at LEAST one duplicate for every page

the above value would require `3200 × log(29) / log(10) ≈ 4680` digits in base-10

## 1.2. Digital recreations

### 1.2.1. using (pseudo) ramdom number generator

the most popular is the website by Jonathan Basile: https://libraryofbabel.info/ there you can also find the technical details and various of Basile’s writings, which are also worth reading

the source code is partially available: https://github.com/librarianofbabel/libraryofbabel.info-algo but very few documentation

other notable recreation is by Tom Snelling: https://libraryofbabel.app/ and source code: https://github.com/tdjsnelling/babel

various Python implementations exist:
- https://github.com/striter-no/TLoB-v2/tree/main/src/LMath
- https://github.com/cakenggt/Library-Of-Pybel/blob/master/library_of_babel.py
- https://github.com/louis-e/LibraryOfBabel-Python/blob/main/main.py

there’re also implementations in many programming languges: Go, Rust, *etc.*

technical read: https://www.reddit.com/r/BabelForum/comments/vph7p3/a_long_dive_into_the_algorithm_some_math_stupid/

#### 1.2.1.1. technical details

as stated above, generate and save all books to be retrieved is impossible

the clever trick is:
- book content is randomly generated on-the-fly based on a book index
- text search is a reverse random-generator to find the book index from text

the algorithm is usually LCG (linear congruential generator) because it’s invertible (therefore bijectivity)

the search text is padded to 3200 characters (*i.e.* 1 page) using spaces or random characters

that string is now a number in base-29, keep this for later

book index is usually in the form `ROOM.WALL.SHELF.BOOK.PAGE` where: `WALL` is an integer 1-4, `SHELF` is an integer 1-5, `BOOK` is an integer 01-32, `PAGE` is an integer 001-410, while `ROOM` can be alphanumeric with nearly unlimited length to represent a base-32 or base-36 integer

the book index is converted to base-10 integer then put through a random-generator to get a very big number (1 918 667 digits in base-10) that can be converted to 1 312 000 digits in base-29

the random-generator must be reversible, *i.e.* we put the search text (base-29 integer) and get bok index

**i got lost with advanced math at this point**, just know that it works!

as a non-native english speaker, i’ve always wanted Unicode-based solutions for multi-language support, but the math complexity is a significant barrier for me

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

the book content is a base-29 integer with 1 312 000 digits, and the book index is simply the same integer converted to base-94 (94 because of 95 printable characters in the 1t ASCII code page excluding the space)

the author goes even further with convert that integer to image, basically base-256<sup>4</sup>: a digit is now a pixel in the RGBA color system

**my wish for multi-language support is now somewhat do-able**

initially, i intended to develop this in Julia, a language i’m currently exploring due to its long-term potential ; however, given the current lack of mature dependencies, i have opted to use Python for this implementation to ensure stability

i also lack design skill to make a beautiful web interface, so i won’t use Javascript

see [DETAILS](2-DETAILS.md) for technical details about this implementation

### 1.3. go beyond text

i also found some versions of Library of Babel for image and music with the same philosophy behind; very worth exploring in the future if i have time
