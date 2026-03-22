# -*- coding: utf-8 -*-

"""
command line interface

not yet implemented, just a placeholder for now
"""

import argparse

def cli():
	parser = argparse.ArgumentParser(description="My Babel CLI")

	txt_grp = parser.add_argument_group("text file arguments")
	txt_grp.add_argument("--input-txt")
	txt_grp.add_argument("--save-book-content-to-txt")
	txt_grp.add_argument("--save-book-position-to-txt")

	img_grp = parser.add_argument_group("image file arguments")
	img_grp.add_argument("--save-book-content-to-img")

	return parser.parse_args()
