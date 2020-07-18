import colorsys

from PIL import Image,ImageStat
from colorthief import ColorThief

from kadai.utils import ColorUtils

# Match XColors
color_hues = (240, 0, 120, 60, 240, 300, 180, 240)

class HueBasedEngine():
    def __init__(self, image):
        self.image = image
        self.color = getDominantColorFromImage(image)

    def generate(self):
        colors = []

        # Generate Dark Color Pallete
        colors.extend(createXorgPallete(self.color, 0.5))
        # Generate Light Color Pallete
        colors.extend(createXorgPallete(self.color, 0.7))

        return colors

def createXorgPallete(color, value):
    pallete = []
    for i in range(len(color_hues)):
        hsv_color = ColorUtils.changeHsvValue(ColorUtils.changeHsvHue(ColorUtils.rgb_to_hsv(color), float(color_hues[i]/360)), value)
        if hsv_color[1] < 0.4:
            hsv_color = ColorUtils.changeHsvSaturation(hsv_color, 0.4)
        if i == 0:
            hsv_color = ColorUtils.changeHsvHue(hsv_color, color[0])
            hsv_color = ColorUtils.changeHsvValue(hsv_color, 0.24*value)
        elif i == (len(color_hues)-1):
            hsv_color = ColorUtils.changeHsvHue(hsv_color, color[0])
            hsv_color = ColorUtils.changeHsvSaturation(hsv_color, 0.02)
        pallete.append(ColorUtils.hsv_to_rgb(hsv_color))
    return pallete

def getDominantColorFromImage(image_path):
    color_cmd = ColorThief(image_path).get_palette
    raw_colors = color_cmd(color_count=2, quality=3)
    return ColorUtils.hsv_to_rgb(ColorUtils.changeHsvValue(ColorUtils.rgb_to_hsv(raw_colors[0]), 0.7))