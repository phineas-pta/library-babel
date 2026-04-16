# -*- coding: utf-8 -*-

"""
PDF output
"""

from typing import TYPE_CHECKING
from pathlib import Path
from fpdf import FPDF

from .utils import save_multiple_books # decorator to transform "save 1 book" function into "save many books"

if TYPE_CHECKING:
	from ..api.book import Book

_default_font_path = Path(__file__).parents[2] / "assets" / "JuliaMono-Regular.ttf" # included with this program


class _MyPdf(FPDF):
	def footer(self):
		self.set_y(-15) # Position cursor at 1.5 cm from bottom
		self.cell(text=f"Page {self.page_no()} / {{nb}}", w=0, align="center") # w=0 the cell extends up to the right margin so center-align possible


@save_multiple_books
def pdf_save_books_content(self: Book, filepath: Path, *, fontpath: Path = _default_font_path) -> None:
	pdf = _MyPdf()
	pdf.set_margin(10)
	pdf.add_font(family="my_font", fname=fontpath)
	pdf.set_font(family="my_font", size=11)
	for i in self.get_lines():
		if isinstance(i, int):
			pdf.add_page()
		else:
			pdf.cell(text=i, w=0, h=6) # TODO: find better way to compute height instead of hard-coded value
			pdf.ln() # line break
	pdf.output(filepath)
