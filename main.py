#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from my_babel_py.find import find_semi_empty_book
from my_babel_py.interface.cli import cli
from my_babel_py.io.txt import txt_save_book_content, txt_save_book_position
from my_babel_py.io.img import img_save_book_content


if __name__ == "__main__":
	args = cli()
	print("Hello, world!")

	with open(args.input_txt, "r", encoding="utf-8") as f:
		txt = f.read()
	book = find_semi_empty_book(txt)[0]
	print(book)

	txt_save_book_content(book, args.save_book_content_to_txt)
	if args.save_book_position_to_txt is not None:
		txt_save_book_position(book, args.save_book_position_to_txt)

	img_save_book_content(book, args.save_book_content_to_img)
