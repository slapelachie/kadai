from kadai.utils import color_utils


class BaseEngine:
    def __init__(self, image_path: str) -> None:
        """
        Arguments:
            image_path (str): The path to the image
        """
        self.image_path = image_path
        self._colors = self.generate()

    def generate(self) -> list:
        raise NotImplementedError

    def get_dominant_color(self) -> list:
        raise NotImplementedError

    def get_palette(self) -> dict:
        # (bg_dark, bg_light, fg_dark, fg_light, default_dark, default_light)
        dark_color_values = (0.1, 0.7, 0.3, 0.9, 0.7, 0.9)
        light_color_values = (0.9, 0.3, 0.7, 0.1, 0.5, 0.3)

        # (black, white, color)
        dark_color_saturations = (0.2, 0.05, None)
        light_color_saturations = (0.5, 0.2, None)

        dark_colors = self._make_pallete(
            self._colors, dark_color_values, dark_color_saturations
        )
        light_colors = self._make_pallete(
            self._colors, light_color_values, light_color_saturations
        )
        return {"dark": dark_colors, "light": light_colors}

    def _make_pallete(self, colors, values, saturations):
        bg_dark, bg_light, fg_dark, fg_light, default_dark, default_light = values
        black, white, color = saturations

        new_colors = {}
        new_colors["color0"] = color_utils.rgb_to_hex(
            color_utils.change_rgb_saturation(
                color_utils.change_rgb_value(colors[0], bg_dark), black
            )
        )
        new_colors["color7"] = color_utils.rgb_to_hex(
            color_utils.change_rgb_saturation(
                color_utils.change_rgb_value(colors[0], bg_light), white
            )
        )
        new_colors["color8"] = color_utils.rgb_to_hex(
            color_utils.change_rgb_saturation(
                color_utils.change_rgb_value(colors[0], fg_dark), black
            )
        )
        new_colors["color15"] = color_utils.rgb_to_hex(
            color_utils.change_rgb_saturation(
                color_utils.change_rgb_value(colors[0], fg_light), white
            )
        )
        for i in range(6):
            new_colors["color{}".format(str(i + 1))] = color_utils.rgb_to_hex(
                color_utils.change_rgb_saturation(
                    color_utils.change_rgb_value(colors[i + 1], default_dark), color
                )
            )
            new_colors["color{}".format(str(i + 9))] = color_utils.rgb_to_hex(
                color_utils.change_rgb_saturation(
                    color_utils.change_rgb_value(colors[i + 1], default_light), color
                )
            )
        return new_colors