import math
import sys
import logging
from PIL import Image, ImageStat

from kadai import log
from kadai.utils import color_utils
from kadai.engine import ColorThiefEngine

logger = log.setup_logger(__name__, log.defaultLoggingHandler(), level=logging.WARNING)


class VibranceEngine(ColorThiefEngine):
    def generate(self) -> None:
        raw_colors = self._gen_colors()
        return sort_colors(raw_colors)


def get_image_brightness(image_path: str) -> tuple:
    image = Image.open(image_path)
    stat = ImageStat.Stat(image)
    r, g, b = stat.mean
    return math.sqrt(0.299 * (r ** 2) + 0.587 * (g ** 2) + 0.114 * (b ** 2))


def sort_by_vibrance(colors: list) -> list:
    """
    Sorts the colors by their vibrance (saturation * brightness(value))

    Arguments:
            colors (list) -- list of rgb colors
    """

    hsv_vibrances = calculate_vibrance_with_list(colors)
    adjusted_colors = sorted(hsv_vibrances, key=lambda x: abs(x[1] - 1))
    return [i[0] for i in adjusted_colors]


def calculate_vibrance(color: tuple) -> float:
    hsv_color = [*color_utils.rgb_to_hsv(color)]
    ideal_brightness = 1

    # Basically the closer the brightness is to the ideal brightness and
    # the higher the saturation is the larger: the output value
    return hsv_color[1] * (
        2
        + (1 - ((hsv_color[2] / ideal_brightness) + (ideal_brightness / hsv_color[2])))
    )


def calculate_vibrance_with_list(colors: list) -> list:
    hsv_vibrances = []
    for i in range(len(colors)):
        vibrance = calculate_vibrance(colors[i])
        hsv_vibrances.append([colors[i], vibrance])
    return hsv_vibrances


def sort_to_list(colors: list, color_list: list) -> list:
    return [i for i in color_list if i in colors]


def sort_colors(colors: list) -> list:
    """
    Sorts the colors based on a sorting algorithim, and returns a list of colors (length of 8)

    Arguments:
            colors (list) -- list of rgb formatted colors
    """

    # Sort by vibrance and get the least vibrant and the 7 most vibrant
    sorted_colors = sort_by_vibrance(colors)
    top_vibrant = sorted_colors[:7]
    return sort_to_list(top_vibrant, colors)


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