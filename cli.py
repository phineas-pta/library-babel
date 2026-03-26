#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
command line interface
"""

from argparse import ArgumentParser
from pathlib import Path
from warnings import warn
from my_babel_py.core.cste import SYS_INFO
from my_babel_py.search import search_semi_empty_book, search_semi_random_book
from my_babel_py.io.txt import txt_save_books_content, txt_save_books_position, txt_load_book_position

try:
	from my_babel_py.io.img import img_load, img_save_books_content
	_img_capability = True
except ModuleNotFoundError:
	_img_capability = False

try:
	from my_babel_py.io.pdf import pdf_save_books_content
	_pdf_capability = True
except ModuleNotFoundError:
	_pdf_capability = False

###############################################################################
#%% parser

PARSER = ArgumentParser(
	description="The extended “Library of Babel” in terminal: search for a book or browse books",
	usage="",
	epilog="By this art you may contemplate the variation of the 8175 letters",
	allow_abbrev=False
)
subparsers = PARSER.add_subparsers(help="available commands", dest="command") # dest is used to know which subcommand is used

#====================================================================

searcher = subparsers.add_parser(name="search", description="search for a book", usage="")
searcher.add_argument(
	"--fill-option", metavar="OPTION", choices=["empty", "random"], default="empty", 
	help="select what characters to fill in case the search text length is less than a book: with whitespace (default - much faster) or with random characters"
)

searcher.add_argument("-i", "--input", required=True, help="text to search OR path to text file")
searcher.add_argument("-o", "--output", type=Path, required=True, metavar="PATH", help="save book content as .TXT file")
searcher.add_argument("-save-pos", action="store_true", help="whether to save book position (room, wall, shelf, book) as another .TXT file")
searcher.add_argument("-save-img", action="store_true", help="whether to save book as .PNG image")
searcher.add_argument("-save-pdf", action="store_true", help="whether to save book as .PDF document")

#====================================================================

browser = subparsers.add_parser(name="browse", description="browse books", usage="")

browser.add_argument("-i", "--input", type=Path, required=True, help="path to book position .TXT file or book image .PNG file (much faster)")
browser.add_argument("-o", "--output", type=Path, required=True, metavar="PATH", help="save book content as .TXT file")
browser.add_argument("-save-img", action="store_true", help="whether to save book as .PNG image")
browser.add_argument("-save-pdf", action="store_true", help="whether to save book as .PDF document")

#====================================================================

subparsers.add_parser(name="info", description="print system info", usage="")

ARGS = PARSER.parse_args()

###############################################################################
#%% main program

match ARGS.command:

	case "search":

		match ARGS.fill_option:
			case "empty":
				search_func = search_semi_empty_book
			case "random":
				warn("take longer time than fill with whitespace")
				search_func = search_semi_random_book
			case _:
				raise ValueError("unknown fill option")

		if (tmp_path := Path(ARGS.input)).is_file():
			with tmp_path.open(mode="r", encoding="utf-8") as f:
				book = search_func(f.read())
		else:
			book = search_func(ARGS.input)
		print(book)

		txt_save_books_content(book, ARGS.output)
		print(f"book content saved to {ARGS.output}")
		if ARGS.save_pos:
			txt_save_books_position(book, ARGS.output.with_stem(ARGS.output.stem + "_POSITION"))
			print("book position saved to text file in the same folder")
		if ARGS.save_img:
			if _img_capability:
				img_save_books_content(book, ARGS.output.with_suffix(".png"))
				print("image saved in the same folder")
			else:
				warn("no image export capability, output aborted")
		if ARGS.save_pdf:
			if _pdf_capability:
				pdf_save_books_content(book, ARGS.output.with_suffix(".pdf"))
				print("pdf saved in the same folder")
			else:
				warn("no pdf export capability, output aborted")

	case "browse":

		match ARGS.input.suffix.lower():
			case ".png":
				book = img_load(ARGS.input)
			case ".txt":
				book = txt_load_book_position(ARGS.input)
			case _:
				raise ValueError("only .TXT or .PNG file supported")
		print(book)

		txt_save_books_content(book, ARGS.output)
		print(f"book content saved to {ARGS.output}")
		if ARGS.save_img:
			if _img_capability:
				img_save_books_content(book, ARGS.output.with_suffix(".png"))
				print("image saved in the same folder")
			else:
				warn("no image export capability, output aborted")
		if ARGS.save_pdf:
			if _pdf_capability:
				pdf_save_books_content(book, ARGS.output.with_suffix(".pdf"))
				print("pdf saved in the same folder")
			else:
				warn("no pdf export capability, output aborted")

	case "info":
		print(SYS_INFO)

	case _:
		raise ValueError("command not found")
