# -*- coding: utf-8 -*-

"""
PNG image output
directly generate a list 256⁴ colors (in RGBA format) will crash python,
so we need to convert to base-256 then group every 4 colors into a pixel
"""

from pathlib import Path
from warnings import warn
from PIL import Image, ImageOps, ExifTags

from ..core import config, utils
from ..api import book

# shortcut
_SIZE = (config.BOOK_IMAGE_SIZE,) * 2
_TAG = ExifTags.Base.UserComment.value # 37510 = 0x9286


def png_save_books_content(self: book.Book, filepath: Path) -> None:
	"""save the content of the book to an image file"""
	tmp = self.pixels # save to a temporary variable to avoid repeatedly re-computing it
	img = Image.new(mode=config.COLOR_MODE, size=_SIZE, color=config.ZERO_COLOR)

	pixel_index = 0
	for i in range(config.BOOK_IMAGE_SIZE):
		for j in range(config.BOOK_IMAGE_SIZE):
			pixel_index = i * config.BOOK_IMAGE_SIZE + j
			if pixel_index < len(tmp):
				img.putpixel((j, i), tuple(tmp[pixel_index])) # note that PIL uses (x, y) coordinates, so we need to swap i and j
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


def _retouch_img(img: Image.Image) -> Image.Image:
	if img.size != _SIZE:
		warn(f"image will be resized to {config.BOOK_IMAGE_SIZE}×{config.BOOK_IMAGE_SIZE}px with padding")
		img = ImageOps.pad(img, size=_SIZE, color=config.ZERO_COLOR, centering=(0, 0))
	if img.mode != config.COLOR_MODE:
		warn("image will be converted to RGBA mode")
		img = img.convert(config.COLOR_MODE)
	return img


def _get_stop_pixel(img: Image.Image) -> int:
	exif = img.getexif()
	try:
		stop_pixel = int(exif[_TAG].split("stop pixel = ")[-1])
	except LookupError:
		warn(f"image exif doesn’t contain info about stop pixel, setting it to {config.MAX_PIXEL_COUNT} (see math details in docs for why this number)")
		stop_pixel = config.MAX_PIXEL_COUNT
	return stop_pixel


def _get_img_array(img: Image.Image) -> list[str]:
	stop_pixel = _get_stop_pixel(img)
	img_array = []
	for i in range(config.BOOK_IMAGE_SIZE):
		for j in range(config.BOOK_IMAGE_SIZE):
			if i * config.BOOK_IMAGE_SIZE + j < stop_pixel:
				color = img.getpixel((j, i)) # note that PIL uses (x, y) coordinates, so we need to swap i and j
				img_array.extend(f"{c:02x}" for c in color) # convert int to 2-digit hex string
				# ATTENTION: extend not append
			else:
				break
		else:
			continue # only executed if the inner loop did NOT break
		break # only executed if the inner loop DID break
	# no need to break loop early since the rest of pixels are very few (< 0.001%), but for programming practice
	return img_array


def png_load(filepath: Path) -> book.Book:
	"""load the content of the book from an image file"""
	img = Image.open(filepath)
	img = _retouch_img(img)
	img_array = _get_img_array(img)
	img.close()
	raw_int = utils.str2int(img_array, config.BYTE_HEX) # convert from base 256 to base 10
	return book.Book(raw_int)
