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
        dark_colors = make_dark_palette(self._colors)
        light_colors = make_light_palette(self._colors)
        return {"dark": dark_colors, "light": light_colors}


def make_dark_palette(colors):
    new_colors = {}
    new_colors["color0"] = color_utils.rgb_to_hex(
        color_utils.change_rgb_saturation(
            color_utils.change_rgb_value(colors[0], 0.1), 0.2
        )
    )
    new_colors["color7"] = color_utils.rgb_to_hex(
        color_utils.change_rgb_saturation(
            color_utils.change_rgb_value(colors[0], 0.7), 0.05
        )
    )
    new_colors["color8"] = color_utils.rgb_to_hex(
        color_utils.change_rgb_saturation(
            color_utils.change_rgb_value(colors[0], 0.3), 0.2
        )
    )
    new_colors["color15"] = color_utils.rgb_to_hex(
        color_utils.change_rgb_saturation(
            color_utils.change_rgb_value(colors[0], 0.9), 0.05
        )
    )
    for i in range(6):
        new_colors["color{}".format(str(i + 1))] = color_utils.rgb_to_hex(
            color_utils.change_rgb_value(colors[i + 1], 0.7)
        )
        new_colors["color{}".format(str(i + 9))] = color_utils.rgb_to_hex(
            color_utils.change_rgb_value(colors[i + 1], 0.9)
        )
    return new_colors


def make_light_palette(colors):
    new_colors = {}
    new_colors["color0"] = color_utils.rgb_to_hex(
        color_utils.change_rgb_saturation(
            color_utils.change_rgb_value(colors[0], 0.1), 0.05
        )
    )
    new_colors["color7"] = color_utils.rgb_to_hex(
        color_utils.change_rgb_saturation(
            color_utils.change_rgb_value(colors[0], 0.7), 0.2
        )
    )
    new_colors["color8"] = color_utils.rgb_to_hex(
        color_utils.change_rgb_saturation(
            color_utils.change_rgb_value(colors[0], 0.3), 0.05
        )
    )
    new_colors["color15"] = color_utils.rgb_to_hex(
        color_utils.change_rgb_saturation(
            color_utils.change_rgb_value(colors[0], 0.9), 0.2
        )
    )
    for i in range(6):
        new_colors["color{}".format(str(i + 1))] = color_utils.rgb_to_hex(
            color_utils.change_rgb_value(colors[i + 1], 0.5)
        )
        new_colors["color{}".format(str(i + 9))] = color_utils.rgb_to_hex(
            color_utils.change_rgb_value(colors[i + 1], 0.3)
        )
    return new_colors