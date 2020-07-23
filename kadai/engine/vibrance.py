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
        brightness = int(get_image_brightness(self.image_path))
        new_cols = adjust_colors(sort_colors(self.raw_colors))
        return [ColorUtils.rgb_to_hex(color) for color in set_bg_fg(new_cols, brightness)]

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
			color = ColorUtils.changeValueFromRGB(color, 0.6)
		else: 
			color = ColorUtils.changeValueFromRGB(color, 0.8)

		colors[i] = color

	return colors

def sort_colors(colors):
	"""
	Sorts the colors based on a sorting algorithim, and returns a list of colors (length of 8)

	Arguments:
		colors (list) -- list of rgb formatted colors
	"""

	# Sort by vibrance and get the least vibrant and the 7 most vibrant
	sorted_colors = sort_by_vibrance(colors)
	top_vibrant = sorted_colors[:8]
	return sort_to_list(top_vibrant, colors)

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

	colors[0] = ColorUtils.changeValueFromRGB(colors[0], scaled_brightness)
	colors[8] = ColorUtils.changeValueFromRGB(colors[8], .6 + scaled_brightness)

	colors[7] = ColorUtils.changeSaturationFromRGB(
		ColorUtils.changeValueFromRGB(colors[7], .85 + scaled_brightness),
		0.1)
	colors[15] = ColorUtils.changeSaturationFromRGB(
		ColorUtils.changeValueFromRGB(colors[15], min(.95 + scaled_brightness, 1)),
		0.1)

	return colors

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
