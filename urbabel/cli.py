#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
command-line interface
"""

from typing import final, Final
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
from warnings import warn

from .core.config import SYS_INFO, MODIFIED_BOURGES_QUOTE, SRC_URL
from .api.search import search_semi_empty_book, search_semi_random_book
from .api.randomize import pick_random_book
from .io import read_png, read_txt_position

###############################################################################

def get_parser() -> ArgumentParser:
	"""Creates and returns the command-line argument parser."""
	parser = ArgumentParser(
		description="The extended “Library of Babel” in terminal: search for a book or browse books",
		epilog=MODIFIED_BOURGES_QUOTE + "\n\n" + SRC_URL,
		formatter_class=RawDescriptionHelpFormatter,
		allow_abbrev=False
	)
	subparsers = parser.add_subparsers(help="available commands", dest="command") # dest is used to know which subcommand is used
	#====================================================================
	# Search Command
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
	# Browse Command
	browser = subparsers.add_parser(name="browse", description="browse books", usage="")
	_grp0 = browser.add_mutually_exclusive_group(required=True)
	_grp0.add_argument("-r", "--random", action="store_true", help="a completely random book")
	_grp0.add_argument("-i", "--input", type=Path, help="path to book position .TXT file or book image .PNG file")
	browser.add_argument("-o", "--output", type=Path, required=True, metavar="PATH", help="save book content as .TXT file")
	browser.add_argument("-save-pos", action="store_true", help="whether to save book position (room, wall, shelf, book) as another .TXT file")
	browser.add_argument("-save-img", action="store_true", help="whether to save book as .PNG image")
	browser.add_argument("-save-pdf", action="store_true", help="whether to save book as .PDF document")
	#====================================================================
	# Info Command
	subparsers.add_parser(name="info", description="print system info", usage="")

	return parser

###############################################################################

@final
class CLI:
	
	def __init__(self, argv: list[str] | None = None) -> None:
		parser = get_parser()
		self.args: Final = parser.parse_args(argv)

	def run(self) -> None:

		match self.args.command:
			case "search":
				self.handle_search()
			case "browse":
				self.handle_browse()
			case "info":
				self.handle_info()

	def handle_search(self) -> None:
		match self.args.fill_option:
			case "empty":
				search_func = search_semi_empty_book
			case "random":
				warn("take longer time than fill with whitespace")
				search_func = search_semi_random_book

		_input = self.args.input
		if (input_path := Path(_input)).is_file():
			books = search_func(input_path.read_text(encoding="utf-8"))
		else:
			books = search_func(_input)

		for book in books:
			self._save_book(book)

	def handle_browse(self) -> None:
		if self.args.random:
			warn("take pretty long time")
			book = pick_random_book()
		else:
			_input = self.args.input
			match _input.suffix.lower():
				case ".png":
					book = read_png(_input)
				case ".txt":
					book = read_txt_position(_input)
				case _:
					raise ValueError("only .TXT or .PNG file supported")

		self._save_book(book)

	def handle_info(self) -> None:
		print(SYS_INFO)

	def _save_book(self, mybook) -> None:
		print(mybook)
		_output = self.args.output
		mybook.save_txt_content(_output)
		if self.args.save_pos:
			mybook.save_txt_position(_output.with_stem(_output.stem + "_POSITION"))
		if self.args.save_img:
			mybook.save_png(_output.with_suffix(".png"))
		if self.args.save_pdf:
			mybook.save_pdf(_output.with_suffix(".pdf"))

###############################################################################

if __name__ == "__main__":
	cli = CLI()
	cli.run()
