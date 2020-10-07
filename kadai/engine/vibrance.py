import math
import sys
import logging
from PIL import Image,ImageStat
from colorthief import ColorThief

from kadai import log
from kadai.utils import ColorUtils

logger = log.setup_logger(__name__, log.defaultLoggingHandler(), level=logging.WARNING)

class VibranceEngine():
    def __init__(self, image_path):
        self.raw_colors = gen_colors(image_path)
        self.image_path = image_path

    def generate(self):
        """
        Generate the palette. Returns a list of hexidecimal colors
        
        Arguments:
            img (str) -- location of the image
        """
        return sort_colors(self.raw_colors)

def get_image_brightness(im_file):
	im = Image.open(im_file)
	stat = ImageStat.Stat(im)
	r,g,b = stat.mean
	return math.sqrt(0.299*(r**2) + 0.587*(g**2) + 0.114*(b**2))

def sort_by_vibrance(colors):
	"""
	Sorts the colors by their vibrance (saturation * brightness(value))

	Arguments:
		colors (list) -- list of rgb colors
	"""

	hsv_distance=calculateVibranceFromList(colors)
	adj_colors = sorted(hsv_distance, key = lambda x:abs(x[1]-1))
	return [i[0] for i in adj_colors]

def calculateVibrance(color):
	hsv_color = [*ColorUtils.rgb_to_hsv(color)]
	ideal_brightness=1

	# Basically the closer the brightness is to the ideal brightness and
	# the higher the saturation is the larger the output value
	return hsv_color[1]*(2+(1-((hsv_color[2]/ideal_brightness)+(ideal_brightness/hsv_color[2]))))	

def calculateVibranceFromList(colors):
	hsv_distance = []
	for i in range(len(colors)):
		vibrance = calculateVibrance(colors[i])
		hsv_distance.append([colors[i], vibrance])
	return hsv_distance

def sort_to_list(colors, color_list):
	return [i for i in color_list if i in colors]

def sort_colors(colors):
	"""
	Sorts the colors based on a sorting algorithim, and returns a list of colors (length of 8)

	Arguments:
		colors (list) -- list of rgb formatted colors
	"""

	# Sort by vibrance and get the least vibrant and the 7 most vibrant
	sorted_colors = sort_by_vibrance(colors)
	top_vibrant = sorted_colors[:7]
	return sort_to_list(top_vibrant, colors)

def gen_colors(image_path):
	"""
	Create a list of colors, max of 16 and min of 8
	
	Arguments:
		img (str) -- location of the image
	"""

	color_cmd = ColorThief(image_path).get_palette
	raw_colors = color_cmd(color_count=16, quality=3)

	if len(raw_colors) <= 8:		
		logger.warn("ColorThief couldn't generate a suitable pallete")
		return None

	return raw_colors

"""
kadai - Simple wallpaper manager for tiling window managers.
Copyright (C) 2020  slapelachie

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Find the full license in the root of this project
"""