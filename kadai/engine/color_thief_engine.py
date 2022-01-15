"""
The base engine for generating colors from colorthief

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
from colorthief import ColorThief

from kadai.engine import BaseEngine
from kadai.utils import color_utils


class ColorThiefEngine(BaseEngine):
    """The base engine for generating colors from colorthief"""

    def __init__(self, image_path: str) -> None:
        super().__init__(image_path)
        self._colors = self.generate()

    def generate(self) -> List[Tuple[int]]:
        raw_colors = self._gen_colors()
        return raw_colors[:7]

    def _gen_colors(self) -> List[Tuple[int]]:
        """
        Create a list of colors, max of 16 and min of 8

        Returns:
            (List[Tuple[int]]): the raw colors
        """
        color_cmd = ColorThief(self._image_path).get_palette
        raw_colors = color_cmd(color_count=16, quality=3)

        if len(raw_colors) <= 8:
            raise Exception("Not enough colors were generated")

        return raw_colors

    def get_dominant_color(self):
        color_cmd = ColorThief(self._image_path).get_palette
        raw_colors = color_cmd(color_count=2, quality=3)
        return color_utils.hsv_to_rgb(
            color_utils.change_hsv_value(color_utils.rgb_to_hsv(raw_colors[0]), 0.7)
        )
