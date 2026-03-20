# Library of Babel

a customized Python CLI version of @zwyx ’s Library of Babel

see [ABOUT](docs/ABOUT.md) for more details about my discovery journey

see [DETAILS](docs/DETAILS.md) for technical details about this implementation

**dependencies**:
- General Multi-Precision (GMP) arithmetic: `gmpy2`: to crunch very big number
- International Components for Unicode (ICU): `pyicu`: to deal with unicode inputs
  - windows wheels can be downloaded from: https://github.com/cgohlke/pyicu-build/releases
  - linux need `libicu-dev` or the like
  - mac need `icu4c`

**usage**:
```bash
python main --help
```

**TODO** (not in any order):
- [ ] better user interface: text / graphical / web
- [ ] PDF output
- [ ] research how to leverage GPU to crunch much bigger number and batch processing
- [ ] Julia verion ?
