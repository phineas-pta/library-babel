#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from my_babel_py.search import search_semi_empty_book, search_semi_random_book
from my_babel_py.interface.cli import cli
from my_babel_py.io.txt import txt_save_books_content, txt_save_books_position
from my_babel_py.io.img import img_load, img_save_books_content


_SEARCH_TYPE = {
	"empty": search_semi_empty_book,
	"random": search_semi_random_book,
}


if __name__ == "__main__":
	args = cli()

	search_func = _SEARCH_TYPE.get(args.fill_option)

	if args.input_query is not None:
		txt = args.input_query
		book = search_func(txt)
	elif args.input_txt_file is not None:
		with open(args.input_txt_file, "r", encoding="utf-8") as f:
			txt = f.read()
		book = search_func(txt)
	elif args.input_img_file is not None:
		book = img_load(args.input_img_file)

	print(f"load {len(book)} books")

	if args.save_book_content_to_txt is not None:
		txt_save_books_content(book, args.save_book_content_to_txt)
	if args.save_book_position_to_txt is not None:
		txt_save_books_position(book, args.save_book_position_to_txt)
	if args.save_book_content_to_img is not None:
		img_save_books_content(book, args.save_book_content_to_img)
