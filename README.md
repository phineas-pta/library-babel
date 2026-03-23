![](https://github.com/tdjsnelling/babel/blob/master/src/public/image/study.png)

# Library of Babel

## about

a Python transpilation of @zwyx ’s Library of Babel: mainly a CLI with limited multi-language input support

for personal fun and also coding challenge

see [ABOUT](docs/1-ABOUT.md) for more details about my exploration journey

see [DETAILS](docs/2-DETAILS.md) for technical details about this implementation

this program is STILL INTENDED FOR PYTHON DEVELOPERS: dependencies installation isn’t trivial for end users

## credits

- this program is built upon https://github.com/zwyx/library-of-babel
- also partially inspired from https://github.com/tdjsnelling/babel by Tom Snelling
- don’t forget the original work of https://github.com/librarianofbabel/libraryofbabel.info-algo by Jonathan Basile

all illustrations in this repo are just links to the website of Jonathan Basile and Tom Snelling

## dependencies

- penultimate stable version of Python recommended (3.13 at the time of writing)
- General Multi-Precision (GMP) arithmetic: `gmpy2`: to crunch very big number
- International Components for Unicode (ICU): `pyicu`: to deal with unicode inputs
  - windows wheels can be downloaded from: https://github.com/cgohlke/pyicu-build/releases
  - linux need `libicu-dev` or the like
  - mac need `icu4c`
- `pillow` to process image

![](https://libraryofbabel.info/img/tower.jpg "the Tower of Babel by Pieter Bruegel the Elder")

## usage

i include a [text file](docs/3-EXTRA.md) that u can use to test the program

```bash
python main.py search --input-txt-file docs/3-EXTRA.md --save-book-content-to-txt draft/book-1.txt --save-book-content-to-img draft/book-1.png
```

on my computer, process a book take ~5s, then save to `.png` take ~2s, RAM usage < 200 MiB

RECOMMENDATION: use a modern monospace file to properly render all characters, like `JuliaMono`, `Fira Code`, `Iosevka`, *etc.*

**extra**: u want to generate books in your language without latin characters ? edit `BOOK_CONTENT_CHARACTERS` in file [`cste.py`](my_babel_py/core/cste.py) to your liking

## licensing

even though this program is under MIT, it uses `GMP` which is under GPLv3

if u want GPL-free, u have to replace `gmpy2` with python native `int`

i use `gmpy2` because i expect to process numbers with millions of digits, but normally python native `int` should be able to do it with lesser performance (need benchmark to verify) so i try to use `gmpy2` as little as possible

## TODO

(not in any particular order)

- [ ] TXT / PNG / PDF input / output
- [ ] verify the number of characters filtered: 8131 in book content, 149625 in book id
- [ ] better user interface: text / graphical / web
- [ ] research how to leverage GPU to crunch much bigger number and batch processing
- [ ] Julia version ?

![](https://github.com/tdjsnelling/babel/blob/master/src/public/image/shelves.png)
