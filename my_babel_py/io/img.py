# -*- coding: utf-8 -*-

"""
image output
directly generate a list 256⁴ colors (in RGBA format) will crash python,
so we need to convert to base-256 then group every 4 colors into a pixel
"""

from PIL import Image
from ..core.book import Book # for typing only
from ..core.cste import BOOK_IMAGE_SIZE

def img_save_book_content(book: Book, filename: str) -> None:
	"""save the content of the book to an image file"""
	tmp = book.img_array # save the content to a temporary variable to avoid repeatedly re-computing it
	img = Image.new(mode="RGBA", size=(BOOK_IMAGE_SIZE, BOOK_IMAGE_SIZE), color=(255,)*4) # white image
	for i in range(BOOK_IMAGE_SIZE):
		for j in range(BOOK_IMAGE_SIZE):
			pixel_index = i * BOOK_IMAGE_SIZE + j
			if pixel_index < len(tmp): # there’re 342px more than enough pixels to store the content of the book
				img.putpixel((j, i), tuple(tmp[i * BOOK_IMAGE_SIZE + j])) # note that PIL uses (x, y) coordinates, so we need to swap i and j
	img.save(filename)
