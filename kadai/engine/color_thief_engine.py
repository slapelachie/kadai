from colorthief import ColorThief

from kadai.engine import BaseEngine
from kadai.utils import color_utils


class ColorThiefEngine(BaseEngine):
    def generate(self):
        raw_colors = self._gen_colors()
        return raw_colors[:7]

    def _gen_colors(self):
        """
        Create a list of colors, max of 16 and min of 8

        Arguments:
                img (str) -- location of the image
        """

        color_cmd = ColorThief(self.image_path).get_palette
        raw_colors = color_cmd(color_count=16, quality=3)

        if len(raw_colors) > 8:
            return raw_colors

    def get_dominant_color(self):
        color_cmd = ColorThief(self.image_path).get_palette
        raw_colors = color_cmd(color_count=2, quality=3)
        return color_utils.hsv_to_rgb(
            color_utils.change_hsv_value(color_utils.rgb_to_hsv(raw_colors[0]), 0.7)
        )
