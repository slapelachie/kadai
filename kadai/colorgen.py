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
from PIL import Image,ImageStat
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
	color[0] = int(color[0]/360)

	color_rgb = [col for col in colorsys.hsv_to_rgb(*color)]
	return [int(col*255) for col in color_rgb]

def darken_color(color, amount):
	"""
	Darken color.

	Arguments:
		color (tupple (size:3)) -- rgb color`
		amount (float) -- value from 0 to 1
	"""

	color = [int(col * (1 - amount)) for col in color]
	return color

def lighten_color(color, amount):
	"""
	Lighten a color.

	Arguments:
		color (tuple (size:3)) -- an rgb color
		amount (float) -- value from 0 to 1
	"""

	color = [int(col + (255 - col) * amount) for col in color]
	return color

def image_brightness(im_file):
	# Converting to RGB because stat.mean excepts r,g,b but with an RGBA file
	# it gets r,g,b,a and fails
	im = Image.open(im_file).convert('RGB')
	stat = ImageStat.Stat(im)
	r,g,b = stat.mean
	return math.sqrt(0.299*(r**2) + 0.587*(g**2) + 0.114*(b**2))

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

	return raw_colors

def sort_by_vibrance(colors):
	"""
	Sorts the colors by their vibrance (saturation * brightness(value))

	Arguments:
		colors (list) -- list of rgb colors
	"""

	hsv_distance=[]

	# Calculate the vibrance of the image
	for i in range(len(colors)):
		hsv_color = [*rgb_to_hsv(colors[i])]
		ideal_brightness=1

		# Basically the closer the brightness is to the ideal brightness and
		# the higher the saturation is the larger the output value

		# Edit 20200413: I have no idea what I was on when I was limiting this,
		# the max should be the greatest
		vibrance=hsv_color[1]*(2+(1-((hsv_color[2]/ideal_brightness)+(ideal_brightness/hsv_color[2]))))

		hsv_distance.append([colors[i], vibrance])

	return sorted(hsv_distance, key = lambda x: abs(x[1]-1))

def adjust_colors(cols):
	"""
	Adjust the colors to be within a range that can be read on a terminal,
	with colors 0-7 being darker then 8-15

	Arguments:
		cols (list) a list of rgb colors
	"""

	colors = [*cols, *cols]
	# Adjust colors
	for i in range(len(colors)):
		color = colors[i]
		if i <= 7:
			while rgb_to_hsv(color)[2] < 0.65:
				color = lighten_color(color, 0.05)
			while rgb_to_hsv(color)[2] > 0.7:
				color = darken_color(color, 0.05)
		else: 
			while rgb_to_hsv(color)[2] < 0.75:
				color = lighten_color(color, 0.05)
			while rgb_to_hsv(color)[2] > 0.8:
				color = darken_color(color, 0.05)

		colors[i] = color

	return colors

def sort_colors(colors):
	"""
	Sorts the colors based on a sorting algorithim, and returns a list of colors (length of 8)

	Arguments:
		colors (list) -- list of rgb formatted colors
	"""

	# Sort by vibrance and get the least vibrant and the 7 most vibrant
	sorted_colors = [x[0] for x in sort_by_vibrance(colors)]
	return [sorted_colors[-1]] + sorted_colors[:7]

def change_value(color, value):
	"""
	Changes the value (in hsv) to the parsed argument

	Arguments:
		color (tuple (size:3)) a rgb color
		value (int) the value of the new color (accepts from 0 to 1 (e.g. 0.53))
	"""

	color_hsv = list(rgb_to_hsv(color))
	color_hsv[2] = value
	return hsv_to_rgb(color_hsv)

def set_bg_fg(colors, brightness):
	"""
	Modifys the background and foreground colors based on the brightness
	of the whole picture

	Arguments:
		colors (list) -- list of rgb colors, expects 8 unique colors
		brightness (int) -- the brightness of the image
	"""

	scaled_brightness = float(brightness/(17*255))
	colors[8] = colors[7] = colors[15] = colors[0]

	colors[0] = change_value(colors[0], scaled_brightness)
	colors[8] = change_value(colors[8], .6 + scaled_brightness)

	colors[7] = change_value(colors[7], .85 + scaled_brightness)
	colors[15] = change_value(colors[15], min(.95 + scaled_brightness, 1))

	return colors


def get(img):
	"""
	Generate the palette. Returns a list of hexidecimal colors
	
	Arguments:
		img (str) -- location of the image
	"""
	cols = gen_colors(img)
	brightness = int(image_brightness(img))
	new_cols = adjust_colors(sort_colors(cols))
	return [rgb_to_hex(color) for color in set_bg_fg(new_cols, brightness)]

def generate(image):
	"""
	Generates the color pallete pased on the image given

	Arguments:
		image (str) -- location of the image
	"""

	# Resize the image so color processing is quicker
	img = Image.open(image)
	image_out = img.resize((300,150), Image.NEAREST)
	image_out.save("/tmp/tmp.png")
	# Generate the pallete based on the small img
	return get('/tmp/tmp.png')