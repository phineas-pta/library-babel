# -*- coding: utf-8 -*-

from ..core.config import CAPABILITIES
from .txt import txt_load_book_position as read_txt_position

if CAPABILITIES["png"]:
	from .png import png_load as read_png
else:
	def read_png(*args, **kwargs):
		print("PNG is not supported, output aborted")
