# -*- coding: utf-8 -*-

"""
image output
directly generate a list 256⁴ colors (in RGBA format) will crash python,
so we need to convert to base-256 then group every 4 colors into a pixel
"""

from pathlib import Path # for typing only
from warnings import warn
from PIL import Image, ImageOps, ExifTags
from .book import Book, save_multiple_books # decorator to transform "save 1 book" function into "save many books"
from .config import BOOK_IMAGE_SIZE, BYTE_HEX, MAX_PIXEL_COUNT, COLOR_MODE, ZERO_COLOR, COLOR_LENGTH, PIXEL_LENGTH
from .utils import int2str, str2int

# shortcut
_SIZE = (BOOK_IMAGE_SIZE,) * 2
_TAG = ExifTags.Base.UserComment.value # 37510 = 0x9286


@save_multiple_books
def img_save_books_content(book: Book, filepath: Path) -> None:
	"""save the content of the book to an image file"""

	tmp = int2str(book.raw_int, BYTE_HEX) # convert to base 256
	if (rem := len(tmp) % PIXEL_LENGTH) != 0: # pad with zeros to make the length a multiple of 8
		tmp = "0" * (PIXEL_LENGTH - rem) + tmp

	img_array = []
	for i in range(0, len(tmp), PIXEL_LENGTH):
		pixel_color = []
		for j in range(0, PIXEL_LENGTH, COLOR_LENGTH):
			color = int(tmp[(i+j):(i+j+COLOR_LENGTH)], base=16) # convert hex to int
			pixel_color.append(color)
		img_array.append(pixel_color)
	assert len(img_array) <= MAX_PIXEL_COUNT * len(COLOR_MODE), "too many more pixels than expected, need to re-do the math"

	img = Image.new(mode=COLOR_MODE, size=_SIZE, color=ZERO_COLOR)
	pixel_index = 0
	for i in range(BOOK_IMAGE_SIZE):
		for j in range(BOOK_IMAGE_SIZE):
			pixel_index = i * BOOK_IMAGE_SIZE + j
			if pixel_index < len(img_array):
				img.putpixel((j, i), tuple(img_array[pixel_index])) # note that PIL uses (x, y) coordinates, so we need to swap i and j
			else:
				break
		else:
			continue # only executed if the inner loop did NOT break
		break # only executed if the inner loop DID break
	# no need to break loop early since the rest of pixels are very few (< 0.005%), but for programming practice

	exif = img.getexif()
	exif[_TAG] = f"stop pixel = {pixel_index}"
	img.save(filepath, exif=exif)
	img.close()


def img_load(filepath: Path) -> Book:
	"""load the content of the book from an image file"""

	img = Image.open(filepath)
	if img.size != _SIZE:
		warn(f"image will be resized to {BOOK_IMAGE_SIZE}×{BOOK_IMAGE_SIZE}px with padding")
		img = ImageOps.pad(img, size=_SIZE, color=ZERO_COLOR, centering=(0, 0))
	if img.mode != COLOR_MODE:
		warn("image will be converted to RGBA mode")
		img = img.convert(COLOR_MODE)
	exif = img.getexif()
	try:
		stop_pixel = int(exif[_TAG].split("stop pixel = ")[-1])
	except (KeyError, IndexError):
		warn(f"image exif doesn’t contain info about stop pixel, setting it to {MAX_PIXEL_COUNT} (see math details in docs for why this number)")
		stop_pixel = MAX_PIXEL_COUNT

	img_array = []
	for i in range(BOOK_IMAGE_SIZE):
		for j in range(BOOK_IMAGE_SIZE):
			if i * BOOK_IMAGE_SIZE + j < stop_pixel:
				color = img.getpixel((j, i)) # note that PIL uses (x, y) coordinates, so we need to swap i and j
				img_array.extend(f"{c:02x}" for c in color) # convert int to 2-digit hex string
				# ATTENTION: extend not append
			else:
				break
		else:
			continue # only executed if the inner loop did NOT break
		break # only executed if the inner loop DID break
	# no need to break loop early since the rest of pixels are very few (< 0.001%), but for programming practice
	img.close()

	raw_int = str2int(img_array, BYTE_HEX) # convert from base 256 to base 10
	book = Book(raw_int=raw_int)
	return book
