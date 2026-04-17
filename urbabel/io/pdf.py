# -*- coding: utf-8 -*-

"""
PDF output
"""

from typing import TYPE_CHECKING
from pathlib import Path
from fpdf import FPDF

if TYPE_CHECKING:
	from ..api.book import Book


class _MyPdf(FPDF):

	def __init__(self, *, fontpath: Path) -> None:
		super().__init__()
		self.set_margin(10)
		self.add_font(family="my_font", fname=fontpath)
		self.set_font(family="my_font", size=11)

	def footer(self) -> None:
		self.set_y(-15) # Position cursor at 1.5 cm from bottom
		self.cell(text=f"Page {self.page_no()} / {{nb}}", w=0, align="center") # w=0 the cell extends up to the right margin so center-align possible


def pdf_save_books_content(self: Book, filepath: Path, *, fontpath: Path | None = None) -> None:
	if fontpath is None:
		fontpath = Path(Path(__file__).parents[2], "assets", "JuliaMono-Regular.ttf") # included with this program
	pdf = _MyPdf(fontpath=fontpath)
	for i in self.get_lines():
		if isinstance(i, int):
			pdf.add_page()
		else:
			pdf.cell(text=i, w=0, h=6) # TODO: find better way to compute height instead of hard-coded value
			pdf.ln() # line break
	pdf.output(filepath)
