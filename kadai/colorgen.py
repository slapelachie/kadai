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

def get_engine_class(engine):
	if engine == "hue":
		from kadai.engine import HueEngine
		return HueEngine
	elif engine == "vibrance":
		from kadai.engine import VibranceEngine
		return VibranceEngine
	else:
		return None

def create_tmp_image(image, path):
	img = Image.open(image)
	image_out = img.resize((150,75), Image.NEAREST).convert('RGB')
	image_out.save(path)

def generate(image, backend):
	"""
	Generates the color pallete pased on the image given

	Arguments:
		image (str) -- location of the image
	"""

	# Resize the image so color processing is quicker
	tmp_file = "/tmp/kadai-tmp.png"
	create_tmp_image(image, tmp_file)

	engine = get_engine_class(backend)
	return engine(tmp_file).generate()