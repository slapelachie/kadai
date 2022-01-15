"""
Generates colors based off of the hue of the primary color

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
from typing import List, Tuple
from kadai.utils import color_utils
from kadai.engine import ColorThiefEngine

# Match XColors
COLOR_HUES = (240, 0, 120, 60, 240, 300, 180)


class HueEngine(ColorThiefEngine):
    """Engine that generates colors based off of the hue of the primary color"""

    def generate(self):
        dominant_color = self.get_dominant_color()
        distance = get_min_distance_hues(dominant_color)
        base_colors = shift_hues_distance(
            generate_base_colors(dominant_color), distance
        )
        return base_colors


def generate_base_colors(color: Tuple[int]) -> List[Tuple[int]]:
    """
    Generates the base colors based on the default hues

    Arguments:
        color (Tuple[int]): the color in rgb format

    Returns:
        (List[Tuple[int]]): a list of rgb colors based off of the default color hues
    """
    new_colors = []
    for color_hue in COLOR_HUES:
        hsv_color = color_utils.change_hsv_hue(
            color_utils.rgb_to_hsv(color), float(color_hue / 360)
        )
        if hsv_color[1] < 0.4:
            hsv_color = color_utils.change_hsv_saturation(hsv_color, 0.4)
        new_colors.append(color_utils.hsv_to_rgb(hsv_color))

    return new_colors


def shift_hues_distance(colors: List[Tuple[int]], distance: float) -> List[Tuple[int]]:
    """
    Shifts a given set of colors hues by a given distance

    Arguments:
        colors (List[Tuple[int]]): the colors in rgb format
        distance (float): the distance to shift

    Returns:
        (List[Tuple[int]]): a set of shifted colors by the given distance
    """
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


def get_min_distance_hues(color: Tuple[int]) -> float:
    """
    Get the minimum distance from a color to one of the default hues

    Arguments:
        color (Tuple[int]): the rgb color

    Returns:
        (float): the minimum distance to one of the default colors
    """
    distances = []
    distances_positive = []
    for color_hue in COLOR_HUES:
        hsv_color = color_utils.rgb_to_hsv(color)

        distance = color_hue - (hsv_color[0] * 360)
        distances.append(distance)
        distances_positive.append(abs(distance))

    min_distance_pos = distances_positive.index(min(distances_positive))
    return float(distances[min_distance_pos] / 360)
