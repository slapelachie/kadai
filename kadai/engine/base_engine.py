from kadai.utils import color_utils


class BaseEngine:
    def __init__(self, image_path: str) -> None:
        """
        Arguments:
            image_path (str): The path to the image
        """
        self._image_path = image_path
        self._colors = None

    def generate(self) -> list:
        """
        Generates a selection of 8 colors from an image

        Returns:
            (list): 8 rgb colors
        """
        raise NotImplementedError

    def get_dominant_color(self) -> tuple:
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

        dark_colors = self._make_palette(
            self._colors, dark_color_values, dark_color_saturations
        )
        light_colors = self._make_palette(
            self._colors, light_color_values, light_color_saturations
        )
        return {"dark": dark_colors, "light": light_colors}

    def _make_palette(self, colors: tuple, values: tuple, saturations: tuple) -> dict:
        """
        Makes a palette that allows modifications to the values and saturation
        Mainly used for xresources and hence uses color 0-15

        Arguments:
            colors (tuple): A list of colors to be made
            values (tuple): How much to change each value by, follows:
                            (bg_dark, bg_light, fg_dark, fg_light, default_dark, default_light)
            saturation (tuple): How much to change the saturation, follows:
                                (black, white, color)

        Returns:
            (dict): A dictionary containing all the colors from 0-15
        """
        new_colors = {}
        bg_dark, bg_light, fg_dark, fg_light, default_dark, default_light = values
        black, white, color = saturations

        new_colors["color0"] = modify_rgb_value_saturation(colors[0], bg_dark, black)
        new_colors["color7"] = modify_rgb_value_saturation(colors[0], bg_light, white)
        new_colors["color8"] = modify_rgb_value_saturation(colors[0], fg_dark, black)
        new_colors["color15"] = modify_rgb_value_saturation(colors[0], fg_light, white)

        for i in range(6):
            new_colors["color{}".format(str(i + 1))] = modify_rgb_value_saturation(
                colors[i + 1], default_dark, color
            )
            new_colors["color{}".format(str(i + 9))] = modify_rgb_value_saturation(
                colors[i + 1], default_light, color
            )

        return new_colors


def modify_rgb_value_saturation(color: tuple, value: float, saturation: float) -> tuple:
    """
    Modifies both the value and saturation of a rgb color

    Arguments:
        color (tuple): the color to be modified
        value (float): what to change the value to
        saturation (float): what to change the saturation to

    Returns:
        (string): The outputed hex value
    """
    return color_utils.rgb_to_hex(
        color_utils.change_rgb_saturation(
            color_utils.change_rgb_value(color, value), saturation
        )
    )