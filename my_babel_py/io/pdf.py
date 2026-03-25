# -*- coding: utf-8 -*-

"""
pdf output
"""

from pathlib import Path # for typing only
from fpdf import FPDF
from ..core.book import Book, save_multiple_books # decorator to transform "save 1 book" function into "save many books"
from ..core.cste import CHARS_PER_LINE, CHARS_PER_PAGE


class myPDF(FPDF):
	def footer(self):
		self.set_y(-15) # Position cursor at 1.5 cm from bottom
		self.cell(text=f"Page {self.page_no()} / {{nb}}", w=0, align="center") # w=0 the cell extends up to the right margin so center-align possible


@save_multiple_books
def pdf_save_books_content(book: Book, filepath: Path) -> None:
	tmp = book.content # save the content to a temporary variable to avoid repeatedly re-computing it
	pdf = myPDF(orientation="portrait", format="A4", unit="mm")
	pdf.set_margin(10)
	pdf.add_font(family="JuliaMono", fname=Path(__file__).parents[2] / "assets" / "JuliaMono-Regular.ttf")
	pdf.set_font(family="JuliaMono", size=11)
	for i in range(0, len(tmp), CHARS_PER_LINE):
		if i % CHARS_PER_PAGE == 0:
			pdf.add_page()
		pdf.cell(text=tmp[i:i+CHARS_PER_LINE], w=0, h=6) # TODO: find better way to compute height instead of hard-coded value
		pdf.ln() # line break
	pdf.output(filepath)
