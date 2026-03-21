# -*- coding: utf-8 -*-

"""
command line interface

not yet implemented, just a placeholder for now
"""

import argparse

def cli():
	parser = argparse.ArgumentParser(description="My Babel CLI")
	parser.add_argument("--input-txt")
	parser.add_argument("--save-book-txt-path")
	return parser.parse_args()
