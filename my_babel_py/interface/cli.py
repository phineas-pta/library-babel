# -*- coding: utf-8 -*-

"""
command line interface

not yet implemented, just a placeholder for now
"""

import argparse
from pathlib import Path

def cli():
	parser = argparse.ArgumentParser(
		description="The extended “Library of Babel” in terminal: search for a book or browse books",
		usage="",
		epilog="By this art you may contemplate the variation of the 8131 letters",
		allow_abbrev=False
	)
	subparsers = parser.add_subparsers()

	###########################################################################

	searcher = subparsers.add_parser(name="search", description="search for a book", usage="")

	input_grp = searcher.add_argument_group(title="input").add_mutually_exclusive_group(required=True)
	input_grp.add_argument("--input-query", metavar="QUERY", help="text to search")
	input_grp.add_argument("--input-txt-file", type=Path, metavar="PATH", help="path to text file")
	input_grp.add_argument("--input-img-file", type=Path, metavar="PATH", help="path to image file")

	output_grp = searcher.add_argument_group(title="output")
	output_grp.add_argument("--save-book-content-to-txt",  type=Path, metavar="PATH", help="path to text file to save book content")
	output_grp.add_argument("--save-book-position-to-txt", type=Path, metavar="PATH", help="path to text file to save book position (room, wall, shelf, book)")
	output_grp.add_argument("--save-book-content-to-img",  type=Path, metavar="PATH", help="path to image file")

	###########################################################################

	browser = subparsers.add_parser(name="browse", description="browse books", usage="")
	browser.add_argument("--nothing", help="not implemented yet")

	return parser.parse_args()
