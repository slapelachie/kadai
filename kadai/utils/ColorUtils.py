import colorsys

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
	new_cols = list(colorsys.rgb_to_hsv(*[float(x/255) for x in color]))
	return tuple(new_cols)

def hsv_to_rgb(color):
	"""
	Converts from hsv to rgb

	Arguments:
		color (list) -- list of hue, saturation, and value for a color [h, s, v]
	"""

	color_rgb = [col for col in colorsys.hsv_to_rgb(*color)]
	return [int(col*255) for col in color_rgb]

def changeHsvValue(color, value):
    return (color[0], color[1], value)

def changeHsvHue(color, hue):
    return (hue, color[1], color[2])

def changeHsvSaturation(color, saturation):
    return (color[0], saturation, color[2])

def changeHueFromRGB(color, hue):
	hsv_color = rgb_to_hsv(color)
	hsv_color = (hue, hsv_color[1], hsv_color[2])
	return hsv_to_rgb(hsv_color)

def changeValueFromRGB(color, value):
	hsv_color = rgb_to_hsv(color)
	hsv_color = (hsv_color[0], hsv_color[1], value)
	return hsv_to_rgb(hsv_color)

def changeSaturationFromRGB(color, saturation):
	hsv_color = rgb_to_hsv(color)
	hsv_color = (hsv_color[0], saturation, hsv_color[2])
	return hsv_to_rgb(hsv_color)

def getHueFromRGB(color):
	hsv_color = rgb_to_hsv(color)
	return hsv_color[0]