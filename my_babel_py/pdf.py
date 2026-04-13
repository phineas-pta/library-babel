# -*- coding: utf-8 -*-

"""
pdf output
"""

from pathlib import Path # for typing only
from fpdf import FPDF
from .book import Book, save_multiple_books # decorator to transform "save 1 book" function into "save many books"
from .config import CHARS_PER_LINE, CHARS_PER_PAGE

_default_font_path = Path(__file__).parents[1] / "assets" / "JuliaMono-Regular.ttf" # included with this program


class MyPdf(FPDF):
	def footer(self):
		self.set_y(-15) # Position cursor at 1.5 cm from bottom
		self.cell(text=f"Page {self.page_no()} / {{nb}}", w=0, align="center") # w=0 the cell extends up to the right margin so center-align possible


@save_multiple_books
def pdf_save_books_content(book: Book, filepath: Path, *, fontpath: Path = _default_font_path) -> None:
	tmp = book.content # save the content to a temporary variable to avoid repeatedly re-computing it
	pdf = MyPdf()
	pdf.set_margin(10)
	pdf.add_font(family="my_font", fname=fontpath)
	pdf.set_font(family="my_font", size=11)
	for i in range(0, len(tmp), CHARS_PER_LINE):
		if i % CHARS_PER_PAGE == 0:
			pdf.add_page()
		pdf.cell(text=tmp[i:i+CHARS_PER_LINE], w=0, h=6) # TODO: find better way to compute height instead of hard-coded value
		pdf.ln() # line break
	pdf.output(filepath)
