import colorsys

from PIL import Image, ImageStat
from colorthief import ColorThief

from kadai.utils import color_utils
from kadai.engine import ColorThiefEngine

# Match XColors
color_hues = (240, 0, 120, 60, 240, 300, 180)


class HueEngine(ColorThiefEngine):
    def generate(self):
        dominant_color = self._get_dominant_color()
        distance = get_min_distance_hues(dominant_color)
        base_colors = shift_hues_distance(
            generate_base_colors(dominant_color), distance
        )
        return base_colors


def generate_base_colors(color):
    new_colors = []
    for i in range(len(color_hues)):
        hsv_color = color_utils.rgb_to_hsv(color)
        hsv_color = color_utils.change_hsv_hue(hsv_color, float(color_hues[i] / 360))
        if hsv_color[1] < 0.4:
            hsv_color = color_utils.change_hsv_saturation(hsv_color, 0.4)
        new_colors.append(color_utils.hsv_to_rgb(hsv_color))
    return new_colors


def shift_hues_distance(colors, distance):
    new_colors = []
    for color in colors:
        hsv_color = color_utils.rgb_to_hsv(color)
        new_hue = hsv_color[0] + distance
        if new_hue >= 1:
            new_hue = new_hue - 1
        elif new_hue < 0:
            new_hue = new_hue + 1
        new_colors.append(color_utils.change_rgb_hue(color, new_hue))
    return new_colors


def get_min_distance_hues(color):
    distances = []
    distances_positive = []
    for color_hue in color_hues:
        hsv_color = color_utils.rgb_to_hsv(color)

        distance = color_hue - (hsv_color[0] * 360)
        distances.append(distance)
        distances_positive.append(abs(distance))

    min_distance_pos = distances_positive.index(min(distances_positive))
    return distances[min_distance_pos] / 360


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