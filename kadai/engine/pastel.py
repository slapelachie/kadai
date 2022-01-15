"""
The engine for generating pastel colors

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
from kadai.engine import VibranceEngine, HueEngine
from kadai.utils import color_utils


class PastelEngine(VibranceEngine):
    """The engine for generating pastel colors"""

    def get_palette(self) -> dict:
        # (bg_dark, bg_light, fg_dark, fg_light, default_dark, default_light)
        dark_color_values = (0.1, 0.7, 0.3, 0.9, 0.9, 1)
        light_color_values = (0.9, 0.3, 0.7, 0.1, 0.6, 0.4)

        # (black, white, color)
        dark_color_saturations = (0.2, 0.05, 0.4)
        light_color_saturations = (0.5, 0.2, 0.4)

        dark_colors = color_utils.make_palette(
            self._colors, dark_color_values, dark_color_saturations
        )
        light_colors = color_utils.make_palette(
            self._colors, light_color_values, light_color_saturations
        )
        return {"dark": dark_colors, "light": light_colors}

    def get_dominant_color(self):
        return color_utils.change_rgb_saturation(
            color_utils.change_rgb_value(super().get_dominant_color(), 1), 0.4
        )


class PastelHueEngine(HueEngine, PastelEngine):
    """Engine for generating colors based of the hues"""

    # TODO: implement this
