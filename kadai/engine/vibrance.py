"""
The engine for generating colors from the most vibrant colors

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
from typing import Tuple, List
from kadai.utils import color_utils
from kadai.engine import ColorThiefEngine


class VibranceEngine(ColorThiefEngine):
    """The engine for generating colors from colorthief"""

    def generate(self) -> None:
        raw_colors = self._gen_colors()
        return sort_colors(raw_colors)


def sort_by_vibrance(colors: List[Tuple[int]]) -> List[Tuple[int]]:
    """
    Sorts the colors by their vibrance (saturation * brightness(value))

    Arguments:
        colors (List[Tuple[int]]): list of rgb colors

    Returns:
        (List[Tuple[int]]): the list sorted by their vibrances
    """

    hsv_vibrances = calculate_vibrance_with_list(colors)
    adjusted_colors = sorted(hsv_vibrances, key=lambda x: abs(x[1] - 1))
    return [i[0] for i in adjusted_colors]


def calculate_vibrance(color: Tuple[int]) -> float:
    """
    Calculate the vibrance of a given color

    Arguments:
        color (Tuple[int]): the rgb color

    Returns:
        (float): the vibrance of the given color
    """
    hsv_color = [*color_utils.rgb_to_hsv(color)]
    ideal_brightness = 1

    # Basically the closer the brightness is to the ideal brightness and
    # the higher the saturation is the larger: the output value
    return hsv_color[1] * (
        2
        + (1 - ((hsv_color[2] / ideal_brightness) + (ideal_brightness / hsv_color[2])))
    )


def calculate_vibrance_with_list(
    colors: List[Tuple[int]],
) -> List[Tuple[Tuple[int], float]]:
    """
    Calculates the vibrances of a list of colors

    Arguments:
        colors (List[Tuple[int]]): a list of rgb colors

    Returns:
        (List[Tuple[Tuple[int], float]]): the list of colors with their vibrances
    """
    hsv_vibrances = []
    for color in colors:
        vibrance = calculate_vibrance(color)
        hsv_vibrances.append([color, vibrance])
    return hsv_vibrances


def sort_to_list(
    colors: List[Tuple[int]], color_list: List[Tuple[int]]
) -> List[Tuple[int]]:
    """
    Return the colors list in the order they appear if they appear in colors

    Arguments:
        colors (List[Tuple[int]]): the original set of colors to sort against
        color_list (List[Tuple[int]]): the set to sort

    Returns:
        (List[Tuple[int]]): the sorted list
    """
    return [i for i in color_list if i in colors]


def sort_colors(colors: List[Tuple[int]]) -> List[Tuple[int]]:
    """
    Sorts the colors based on a sorting algorithim, and returns a list of colors (length of 7)

    Arguments:
        colors (List[Tuple[int]]): list of rgb formatted colors

    Returns:
        (List[Tuple[int]]): the sorted list of rgb colors
    """

    # Sort by vibrance and get the least vibrant and the 7 most vibrant
    sorted_colors = sort_by_vibrance(colors)
    top_vibrant = sorted_colors[:7]
    return sort_to_list(top_vibrant, colors)
