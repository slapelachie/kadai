#!/usr/bin/env python3

# colorgen
# Author: slapelachie
# Note: Most of this code is from pywal, but is modified to get a greater range of colors from 
# the top 16 colors of the wallpaper
#

import logging
import sys
import colorsys
import sys, getopt
import math
from PIL import Image
from colorthief import ColorThief

from . import log

logger = log.setup_logger(__name__, logging.INFO, log.defaultLoggingHandler())

inputfile = ''
argv=sys.argv[1:]

def rgb_to_hex(color):
	"""
	Convert an rgb color to hex.

	Arguments:
		color (list) -- list of red, green, and blue for a color [r, g, b]
	"""

	return "#%02x%02x%02x" % (*color,)

def rgb_to_yiq(color):
	"""
	Converts from rgb to yiq

	Arguments:
		color (list) -- list of red, green, and blue for a color [r, g, b]
	"""

	return colorsys.rgb_to_yiq(*hex_to_rgb(color))

def rgb_to_hsv(color):
	"""
	Converts from rgb to hsv

	Arguments:
		color (list) -- list of red, green, and blue for a color [r, g, b]
	"""
	new_cols = list(colorsys.rgb_to_hsv(*[float(x/256) for x in color]))
	new_cols[0] = int(new_cols[0]*360)
	return tuple(new_cols)

def hsv_to_rgb(color):
	"""
	Converts from hsv to rgb

	Arguments:
		color (list) -- list of hue, saturation, and value for a color [h, s, v]
	"""

	return [int(col) for col in colorsys.hsv_to_rgb(*color)]

def rgb_to_hls(color):
	"""
	Converts from rgb to hsv

	Arguments:
		color (list) -- list of red, green, and blue for a color [r, g, b]
	"""
	return colorsys.rgb_to_hls(*color)

def hls_to_rgb(color):
	"""
	Converts from hsv to rgb

	Arguments:
		color (list) -- list of hue, saturation, and value for a color [h, s, v]
	"""

	return [int(col) for col in colorsys.rgb_to_hls(*color)]

def hex_to_rgb(color):
	"""
	Convert a hex color to rgb.

	Arguments:
		color (string) -- hexadecimal value with the leading '#'
	"""

	return tuple(bytes.fromhex(color.strip("#")))

def darken_color(color, amount):
	"""
	Darken a hex color.

	Arguments:
		color (string) -- hexadecimal value with the leading '#'
		amount (float) -- value from 0 to 1
	"""

	color = [int(col * (1 - amount)) for col in hex_to_rgb(color)]
	return rgb_to_hex(color)

def lighten_color(color, amount):
	"""
	Lighten a hex color.

	Arguments:
		color (string) -- hexadecimal value with the leading '#'
		amount (float) -- value from 0 to 1
	"""

	color = [int(col + (255 - col) * amount) for col in hex_to_rgb(color)]
	return rgb_to_hex(color)

def gen_colors(img):
	"""
	Create a list of colors, max of 16 and min of 8
	
	Arguments:
		img (str) -- location of the image
	"""

	color_cmd = ColorThief(img).get_palette
	raw_colors = color_cmd(color_count=16, quality=3)

	if len(raw_colors) <= 8:
		logger.error("ColorThief couldn't generate a suitable palette.")
		sys.exit(1)

	return [rgb_to_hex(color) for color in raw_colors]

def sort_by_vibrance(cols):
	"""
	Determines the distance of a list of colors from a color

	Arguments:
		cols (list) -- list of hexidecimal formatted colors
	"""

	hls_distance=[]

	# Calculate the vibrance of the image
	for i in range(len(cols)):
		hls_color = [*rgb_to_hls(hex_to_rgb(cols[i]))]
		vibrance = (hls_color[2])

		hls_distance.append([cols[i], vibrance])

	return sorted(hls_distance, key = lambda x: abs(x[1]-1))

def adjust_colors(colors):
	# Adjust colors
	for i in range(len(colors)):
		if i != 0 and i != 7:    
			col=hex_to_rgb(colors[i])
			if i <= 7:
				while rgb_to_hsv(col)[2] < 0.7:
					col = hex_to_rgb(lighten_color(rgb_to_hex(col), 0.05))
				while rgb_to_hsv(col)[2] > 0.75:
					col = hex_to_rgb(darken_color(rgb_to_hex(col), 0.05))
			else: 
				while rgb_to_hsv(col)[2] < 0.8:
					 col = hex_to_rgb(lighten_color(rgb_to_hex(col), 0.05))
				while rgb_to_hsv(col)[2] > 0.85:
					 col = hex_to_rgb(darken_color(rgb_to_hex(col), 0.05))

			colors[i] = rgb_to_hex(col)

	return colors



def sort_colors(cols, sort_type):
	"""
	Attempts at creating a palette with unique colors

	This barely works correctly and sometimes the colors generated
	are the same

	Arguments:
		cols (list) -- list of hexidecimal formatted colors
		sort_type (string) -- the type of sort to appy
	"""

	if sort_type == "VIBRANCE":
		# Sort by vibrance and get the least vibrant and the 7 most vibrant
		sorted_cols = [x[0] for x in sort_by_vibrance(cols)]
		new_cols=[sorted_cols[0]] + sorted_cols[len(sorted_cols)-7:]

		# Sort back to order of dominant colors
		return [x for x in cols if x in new_cols]
	#elif sort_type == "MATCH":
	#	base_colors = ["#000000", "#ff6565", "#93d44f", ""]

def set_bg_fg(cols):
	"""
	Create and fine tune the palette

	Arguments:
		cols (list) -- list of hexidecimal formatted colors, expects 8 unique colors
	"""

	# Brings the last color to the front, as it is the least vibrant
	# and good for backgrounds

	raw_colors = [*cols, *cols]

	# Darken the blacks
	raw_colors[0] = darken_color(cols[0], 0.95)
	raw_colors[8] = darken_color(cols[0], 0.75)        

	# Whiten the whites
	raw_colors[7] = lighten_color(cols[0], 0.90)
	raw_colors[15] = lighten_color(cols[0], 0.70)

	return raw_colors


def get(img):
	"""
	Generate the palette.
	
	Arguments:
		img (str) -- location of the image
	"""
	cols = gen_colors(img)
	new_cols = sort_colors(adjust_colors(cols), 'VIBRANCE')
	return set_bg_fg(new_cols)


def generate(image):
	"""
	Generates the color pallete pased on the image given

	Arguments:
		image (str) -- location of the image
	"""

	# Resize the image so color processing is quicker
	image = Image.open(image)
	image_out = image.resize((300,150), Image.NEAREST)
	image_out.save("/tmp/tmp.png")
	# Generate the pallete based on the small img
	return get('/tmp/tmp.png')