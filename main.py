#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from my_babel_py.find import find_semi_empty_book
from my_babel_py.interface.cli import cli
from my_babel_py.output.txt import save_txt


if __name__ == "__main__":
	args = cli()
	print("Hello, world!")
	with open(args.input_txt, "r", encoding="utf-8") as f:
		txt = f.read()
	book = find_semi_empty_book(txt)[0]
	print(book)
	save_txt(book, args.save_book_txt_path)
