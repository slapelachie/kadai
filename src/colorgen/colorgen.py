#!/usr/bin/env python3

# colorgen
# Author: slapaay
# Note: Most of this code is from pywal, but is modified to get a greater range of colors from 
# the top 16 colors of the wallpaper
#
# Any print statements made in this script will be inputed into the color scheme file, so do
# not print anything but the colors needed.

import logging
import sys
import colorsys
import sys, getopt
import math
from PIL import Image
from colorthief import ColorThief

inputfile = ''
argv=sys.argv[1:]

# Converts from RGB to HEX
# Accepts in the format of [r, g, b]
def rgb_to_hex(color):
	"""Convert an rgb color to hex."""
	return "#%02x%02x%02x" % (*color,)

# Converts from RGB to YIQ
# Accepts in the format of [r, g, b]
def rgb_to_yiq(color):
	"""Sort a list of colors."""
	return colorsys.rgb_to_yiq(*hex_to_rgb(color))

# Converts from RGB to HSV
# Accepts in the format of [r, g, b]
def rgb_to_hsv(color):
	return colorsys.rgb_to_hsv(*color)

# Converts from HSV to RGB
# Accepts in the format of [h, s, v]
def hsv_to_rgb(color):
	return [int(col) for col in colorsys.hsv_to_rgb(*color)]

# Converts from HEX to RGB
# Accepts in the format of a 6 character string with a '#'
def hex_to_rgb(color):
	"""Convert a hex color to rgb."""
	return tuple(bytes.fromhex(color.strip("#")))

# Darkens a specified color
# arg color: HEX color
# arg amount: float from 0 to 1
def darken_color(color, amount):
	"""Darken a hex color."""
	color = [int(col * (1 - amount)) for col in hex_to_rgb(color)]
	return rgb_to_hex(color)

# Lightens a specified color
# arg color: HEX color
# arg amount: float from 0 to 1
def lighten_color(color, amount):
	"""Lighten a hex color."""
	color = [int(col + (255 - col) * amount) for col in hex_to_rgb(color)]
	return rgb_to_hex(color)

# Generate colors using ColorTheif
# arg img: path/to/image
def gen_colors(img):
	"""Loop until 16 colors are generated."""
	color_cmd = ColorThief(img).get_palette
	raw_colors = color_cmd(color_count=16, quality=3)

	if len(raw_colors) <= 8:
		logging.error("ColorThief couldn't generate a suitable palette.")
		sys.exit(1)

	return [rgb_to_hex(color) for color in raw_colors]

# Determines the distance of a list of colors from a color
# arg col: HEX color
# arg cols: [HEX color]
def get_color_distance(cols):
	hsv_distance=[]

	for i in range(len(cols)):
		hsv_color = [*rgb_to_hsv(hex_to_rgb(cols[i]))]
		vibrance = (hsv_color[1])

		hsv_distance.append([cols[i], math.sqrt(pow(0 -vibrance, 2))])

	return hsv_distance

# Creates a palette with the greatest varience
# arg cols: [HEX color]
def palette_varience(cols):
	distance = get_color_distance(cols)
	sorted_cols = sorted(distance, key = lambda x: x[1])

	for i in range (len(sorted_cols)):
		sorted_cols[i]=sorted_cols[i][0]

	new_cols=[sorted_cols[0]]
	new_cols = new_cols + sorted_cols[len(sorted_cols)-7:]

	# Sort back to order of dominant colors
	dom_sort_cols = []
	for i in cols:
		for j in new_cols:
			if j == i:
				dom_sort_cols.append(i)

	return dom_sort_cols

# Adjusts the colors to make visible on terminal
# arg cols: [HEX color] list length expected to be 8
def adjust(cols):
	"""Create palette."""
	last_col = cols[-1]
	cols = cols[:-1]
	cols.insert(0,last_col)
	raw_colors = [*cols, *cols]

	raw_colors[0] = darken_color(cols[0], 0.95)
	raw_colors[8] = darken_color(cols[0], 0.75)        

	# Lighten other colors
	for i in range(len(raw_colors)):
		if i != 0 and i != 7:    
			col=hex_to_rgb(raw_colors[i])
			if i <= 7:
				while (col[0] + col[1] + col[2]) < 350:
					col = hex_to_rgb(lighten_color(rgb_to_hex(col), 0.05))
			else: 
				while (col[0] + col[1] + col[2]) < 250:
					 col = hex_to_rgb(lighten_color(rgb_to_hex(col), 0.05))
				while (col[0] + col[1] + col[2]) > 300:
					 col = hex_to_rgb(darken_color(rgb_to_hex(col), 0.05))

			raw_colors[i] = rgb_to_hex(col)
	raw_colors[7] = lighten_color(cols[0], 0.90)
	raw_colors[15] = lighten_color(cols[0], 0.70)

	return raw_colors


# Get the colorscheme
# arg img: path/to/image
def get(img):
	"""Get colorscheme."""
	cols = gen_colors(img)
	new_cols = palette_varience(cols)
	return adjust(new_cols)

class ColorGen:
	def generate(self):
 	   # Resize the image so color processing is quicker
		image = Image.open(self)
		image_out = image.resize((300,150), Image.NEAREST)
		image_out.save("/tmp/tmp.png")
		return get('/tmp/tmp.png') 
