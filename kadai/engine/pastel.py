from kadai.engine import VibranceEngine, HueEngine
from kadai.utils import color_utils


class PastelEngine(VibranceEngine):
    def generate(self):
        return super().generate()

    def get_palette(self) -> dict:
        # (bg_dark, bg_light, fg_dark, fg_light, default_dark, default_light)
        dark_color_values = (0.1, 0.7, 0.3, 0.9, 0.9, 1)
        light_color_values = (0.9, 0.3, 0.7, 0.1, 0.6, 0.4)

        # (black, white, color)
        dark_color_saturations = (0.2, 0.05, 0.4)
        light_color_saturations = (0.5, 0.2, 0.4)

        dark_colors = self._make_pallete(
            self._colors, dark_color_values, dark_color_saturations
        )
        light_colors = self._make_pallete(
            self._colors, light_color_values, light_color_saturations
        )
        return {"dark": dark_colors, "light": light_colors}

    def get_dominant_color(self):
        return color_utils.change_rgb_saturation(
            color_utils.change_rgb_value(super().get_dominant_color(), 1), 0.4
        )


class PastelHueEngine(HueEngine, PastelEngine):
    def generate(self):
        return super().generate()