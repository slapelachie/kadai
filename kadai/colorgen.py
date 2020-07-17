#!/usr/bin/env python3

# colorgen
# Author: slapelachie
# Note: Most of this code is from pywal, but is modified to get a greater range of colors from 
# the top 8 colors with a better algorithim
#
# Use kadai.colorgen.generate('file.png') to get hex colors suited for Xdefault colors

import logging
import sys
from PIL import Image

from kadai.engine.vibrance import VibranceEngine

inputfile = ''
argv=sys.argv[1:]

def generate(image):
	"""
	Generates the color pallete pased on the image given

	Arguments:
		image (str) -- location of the image
	"""

	# Resize the image so color processing is quicker
	img = Image.open(image)
	image_out = img.resize((150,75), Image.NEAREST).convert('RGB')
	image_out.save("/tmp/tmp.png")
	# Generate the pallete based on the small img
	vibranceEngine = VibranceEngine('/tmp/tmp.png')
	return vibranceEngine.generate()