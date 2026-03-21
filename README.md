# Library of Babel

## about

a Python transpilation of @zwyx ’s Library of Babel: mainly a CLI with limited multi-language input support

for personal fun and also coding challenge

see [ABOUT](docs/1-ABOUT.md) for more details about my discovery journey

see [DETAILS](docs/2-DETAILS.md) for technical details about this implementation

this program is STILL INTENDED FOR PYTHON DEVELOPPERS: dependencies installation isn’t trivial

## credits

- this program is built upon https://github.com/zwyx/library-of-babel
- also partially inspired from https://github.com/tdjsnelling/babel
- don’t forget the original work of https://github.com/librarianofbabel/libraryofbabel.info-algo

## dependencies

- General Multi-Precision (GMP) arithmetic: `gmpy2`: to crunch very big number
- International Components for Unicode (ICU): `pyicu`: to deal with unicode inputs
  - windows wheels can be downloaded from: https://github.com/cgohlke/pyicu-build/releases
  - linux need `libicu-dev` or the like
  - mac need `icu4c`

## usage

```bash
python main.py --help
```

## licensing

eventhough this program is under MIT, it uses `GMP` which is under GPLv3

i use `gmpy2` because i expect to process numbers with millions of digits, but normally python native `int` should be able to do it with lesser performance (need benchmark to verify) so i try to use `gmpy2` as little as possible

u may want to replace `gmpy2` with python native `int`

## TODO

(not in any particular order)

- [ ] find better way to deal with punctuation & symbols: i can keep them in transliteration but don’t how to properly retrieve all unicode characters
- [ ] TXT / PDF output
- [ ] input support for computer language: programming, markup, data, *etc.*
- [ ] better user interface: text / graphical / web
- [ ] research how to leverage GPU to crunch much bigger number and batch processing
- [ ] Julia verion ?
