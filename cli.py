# -*- coding: utf-8 -*-

"""
command line interface
"""

from argparse import ArgumentParser
from pathlib import Path
from my_babel_py.core.cste import SYS_INFO
from my_babel_py.search import search_semi_empty_book, search_semi_random_book
from my_babel_py.io.txt import txt_save_books_content, txt_save_books_position
from my_babel_py.io.img import img_load, img_save_books_content

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

#====================================================================

browser = subparsers.add_parser(name="browse", description="browse books", usage="")

browser.add_argument("-i", "--input", type=Path, required=True, help="path to book content .TXT or .PNG file")
browser.add_argument("-o", "--output", type=Path, required=True, metavar="PATH", help="save book content as .TXT file")
browser.add_argument("-img", action="store_true", help="whether to save book as .PNG image")

#====================================================================

subparsers.add_parser(name="info", description="print system info", usage="")

ARGS = PARSER.parse_args()

###############################################################################
#%% main program

match ARGS.command:

	case "search":
		_SEARCH_TYPE = {
			"empty": search_semi_empty_book,
			"random": search_semi_random_book,
		}
		search_func = _SEARCH_TYPE.get(ARGS.fill_option)

		if (tmp_path := Path(ARGS.input)).is_file():
			with tmp_path.open(mode="r", encoding="utf-8") as f:
				book = search_func(f.read())
		else:
			book = search_func(ARGS.input)

		txt_save_books_content(book, ARGS.output)
		print(f"book content saved to {ARGS.output}")
		if ARGS.save_pos:
			txt_save_books_position(book, ARGS.output.with_stem(ARGS.output.stem + "_POSITION"))
			print("book position saved to text file in the same folder")
		if ARGS.save_img:
			img_save_books_content(book, ARGS.output.with_suffix(".png"))
			print("image saved in the same folder")

	case "browse":
		match ARGS.input.suffix.lower():
			case ".png":
				book = img_load(ARGS.input_img_file)
			case ".txt":
				pass
			case _:
				raise ValueError("only .TXT or .PNG file supported")

		txt_save_books_content(book, ARGS.output)
		print(f"book content saved to {ARGS.output}")
		if ARGS.save_img:
			img_save_books_content(book, ARGS.output.with_suffix(".png"))
			print("image saved in the same folder")

	case "info":
		print(SYS_INFO)

	case _:
		raise ValueError("command not found")
