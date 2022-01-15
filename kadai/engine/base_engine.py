"""
The base engine for generating colors

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


class BaseEngine:
    """The base engine for generating colors"""

    def __init__(self, image_path: str):
        """
        Arguments:
            image_path (str): The path to the image
        """
        self._image_path = image_path
        self._colors = None

    def generate(self) -> List[Tuple[int]]:
        """
        Generates a selection of 8 colors from an image

        Returns:
            (list): 8 rgb colors
        """
        raise NotImplementedError

    def get_dominant_color(self) -> Tuple[int]:
        """Returns the most dominant rgb color in the image"""
        raise NotImplementedError

    def get_palette(self) -> dict:
        """
        Get a palette of light and dark colors for their respective themes

        Returns:
            (dict): The geneterated color palette
        """

        # (bg_dark, bg_light, fg_dark, fg_light, default_dark, default_light)
        dark_color_values = (0.1, 0.7, 0.3, 0.9, 0.7, 0.9)
        light_color_values = (0.9, 0.3, 0.7, 0.1, 0.5, 0.3)

        # (black, white, color)
        dark_color_saturations = (0.2, 0.05, None)
        light_color_saturations = (0.5, 0.2, None)

        dark_colors = color_utils.make_palette(
            self._colors, dark_color_values, dark_color_saturations
        )
        light_colors = color_utils.make_palette(
            self._colors, light_color_values, light_color_saturations
        )
        return {"dark": dark_colors, "light": light_colors}
