# -*- coding: utf-8 -*-

"""
image output
directly generate a list 256⁴ colors (in RGBA format) will crash python,
so we need to convert to base-256 then group every 4 colors into a pixel
"""

from pathlib import Path # for typing only
from PIL import Image
from PIL.ExifTags import Base
from ..core.book import Book, save_multiple_books # decorator to transform "save 1 book" function into "save many books"
from ..core.cste import BOOK_IMAGE_SIZE, BYTE_HEX
from ..core.utils import int2str, str2int

_MODE = "RGBA"
_TAG = Base.UserComment.value # 37510 = 0x9286


@save_multiple_books
def img_save_books_content(book: Book, filepath: Path) -> None:
	"""save the content of the book to an image file"""

	tmp = int2str(book._raw_int, BYTE_HEX) # convert to base 256
	if (rem := len(tmp) % 8) != 0: # pad with zeros to make the length a multiple of 8
		tmp = "0" * (8 - rem) + tmp

	img_array = []
	for i in range(0, len(tmp), 8): # 4 colors × 2 hex characters per color = 8 characters
		pixel_color = []
		for j in range(0, 8, 2): # 2 hex characters per color
			color = int(tmp[(i+j):(i+j+2)], base=16) # convert hex to int
			pixel_color.append(color)
		img_array.append(pixel_color)

	img = Image.new(mode=_MODE, size=(BOOK_IMAGE_SIZE, BOOK_IMAGE_SIZE), color=(255,)*4) # white image
	for i in range(BOOK_IMAGE_SIZE):
		for j in range(BOOK_IMAGE_SIZE):
			pixel_index = i * BOOK_IMAGE_SIZE + j
			if pixel_index < len(img_array): # there’re at much 342px too many to store the content of the book
				img.putpixel((j, i), tuple(img_array[pixel_index])) # note that PIL uses (x, y) coordinates, so we need to swap i and j
			else:
				break
		else:
			continue # only executed if the inner loop did NOT break
		break # only executed if the inner loop DID break
	# no need to break loop early since the rest of pixels are very few (< 0.06%), but for programming practice

	exif = img.getexif()
	exif[_TAG] = f"stop pixel = {pixel_index}"
	img.save(filepath, exif=exif)
	img.close()


def img_load(filepath: Path) -> Book:
	"""load the content of the book from an image file"""

	img = Image.open(filepath)
	assert img.size == (BOOK_IMAGE_SIZE,)*2, f"the image size must be {BOOK_IMAGE_SIZE}x{BOOK_IMAGE_SIZE}px"
	if img.mode != _MODE:
		img = img.convert(_MODE)
	exif = img.getexif()
	stop_pixel = int(exif[_TAG].split("stop pixel = ")[-1])

	img_array = []
	for i in range(BOOK_IMAGE_SIZE):
		for j in range(BOOK_IMAGE_SIZE):
			if i * BOOK_IMAGE_SIZE + j < stop_pixel: # there’re at much 342px too many to store the content of the book
				color = img.getpixel((j, i)) # note that PIL uses (x, y) coordinates, so we need to swap i and j
				img_array.extend([f"{c:02x}" for c in color]) # convert int to 2-digit hex string
				# ATTENTION: extend not append
			else:
				break
		else:
			continue # only executed if the inner loop did NOT break
		break # only executed if the inner loop DID break
	# no need to break loop early since the rest of pixels are very few (< 0.06%), but for programming practice
	img.close()

	raw_int = str2int(img_array, BYTE_HEX) # convert from base 256 to base 10
	book = Book(raw_int)
	return book
