![](https://github.com/tdjsnelling/babel/blob/master/src/public/image/study.png)

# Library of Babel

![](https://img.shields.io/github/license/phineas-pta/library-babel?style=for-the-badge)
![](https://img.shields.io/badge/python-≥3.14-FF7139?style=for-the-badge)
![](https://img.shields.io/github/languages/code-size/phineas-pta/library-babel?style=for-the-badge&logo=github)
![](https://img.shields.io/github/repo-size/phineas-pta/library-babel?style=for-the-badge&logo=github)
![](https://img.shields.io/badge/hosted_by-localhost-FF4500?style=for-the-badge&logo=serverless)
![](https://img.shields.io/badge/quality-trust_me_bro-DB1?style=for-the-badge)
![](https://img.shields.io/badge/works_on-my_machine-3DDC84?style=for-the-badge)
![](https://img.shields.io/badge/coverage---Inf-F73?style=for-the-badge)
![](https://img.shields.io/badge/code_style-mine-0052CC?style=for-the-badge)
![](https://img.shields.io/badge/built_with-gramma’s_recipe-E43?style=for-the-badge)
![](https://img.shields.io/badge/contains-tasty_spaghetti_code-330F63?style=for-the-badge)
![](https://img.shields.io/badge/contains-techinical_debt-4EA94B?style=for-the-badge)
![](https://img.shields.io/badge/powered_by-electricity-20BEFF?style=for-the-badge)
![](https://img.shields.io/badge/only_installable_by_smelly_nerds-yes-E44C30?style=for-the-badge)

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

- Python version ≥ 3.14 (free-threading not required)
- General Multi-Precision (GMP) arithmetic: `gmpy2`: to crunch very big number
- International Components for Unicode (ICU): `pyicu`: to deal with unicode inputs
  - windows wheels can be downloaded from: https://github.com/cgohlke/pyicu-build/releases
  - linux need `libicu-dev` or the like
  - mac need `icu4c`
- *optional* `pillow` to output image
- *optional* `fpdf2` to output pdf, using `JuliaMono` typeface from https://github.com/cormullion/juliamono

command example **on my machine** (windows):
```bash
pip install pillow gmpy2 fpdf2 https://github.com/cgohlke/pyicu-build/releases/download/v2.16.2/pyicu-2.16.2-cp314-cp314-win_amd64.whl
```

command example on Linux or Mac (`conda` may be easier):
```bash
pip install pillow gmpy2 fpdf2 pyicu
```

![](https://libraryofbabel.info/img/tower.jpg "the Tower of Babel by Pieter Bruegel the Elder")

## usage

i include a [text file](docs/3-EXTRA.md) that u can use to test the program

```bash
python main-cli.py search -i docs/3-EXTRA.md -o tmp/book-1.txt -save-pos -save-img -save-pdf
```

on my computer, process a book take ~3s, then save to `.png` take ~2s, RAM usage < 200 MiB

RECOMMENDATION: use a modern monospace file to properly render all characters, like `JuliaMono`, `Fira Code`, `Iosevka`, *etc.*

COMPATIBILITY: see https://github.com/unicode-org/last-resort-font

**extra 1**: to generate books in your own language without latin characters: edit:
- `BOOK_CONTENT_CHARACTERS` in file [`config.py`](core/config.py)
- `_TRANSLITERATOR` in file [`utils.py`](core/utils.py)

**extra 2**: to change font in PDF output: edit path to font file in [`pdf.py`](io/pdf.py)

## TODO

(not in any particular order)

- [x] TXT / PNG / PDF input / output
- [x] setup github / gitlab ci/cd to automate testing
- [ ] better user interface: text / graphical / web
- [ ] verify the number of characters filtered: ~~8175~~ 8145 in book content, ~~149625~~ 159613 in book id
- [ ] ~~GPU acceleration for base conversion~~ *maybe not really necessary*
- [ ] ~~Julia version ?~~ *not worth the effort at the moment*

![](https://github.com/tdjsnelling/babel/blob/master/src/public/image/shelves.png)
