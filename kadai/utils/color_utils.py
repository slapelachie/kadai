import colorsys
from PIL import Image, ImageDraw


def rgb_to_hex(color: tuple) -> str:
    """
    Convert an rgb color to hex.

    Arguments:
        color (list) -- list of red, green, and blue for a color [r, g, b]
    """

    return "#%02x%02x%02x" % (*color,)


def hex_to_rgb(color: str) -> tuple:
    """
    Convert a hex color to rgb.
    Arguments:
        color (string) -- hexadecimal value with the leading '#'
    """

    return tuple(bytes.fromhex(color.strip("#")))


def rgb_to_hsv(color: tuple) -> tuple:
    """
    Converts from rgb to hsv

    Arguments:
        color (list) -- list of red, green, and blue for a color [r, g, b]
    """
    return tuple(colorsys.rgb_to_hsv(*[float(x / 255) for x in color]))


def hsv_to_rgb(color: tuple) -> tuple:
    """
    Converts from hsv to rgb

    Arguments:
        color (list) -- list of hue, saturation, and value for a color [h, s, v]
    """

    color_rgb = list(colorsys.hsv_to_rgb(*color))
    return tuple(int(col * 255) for col in color_rgb)


def change_hsv_hue(color: tuple, hue: float) -> tuple:
    """
    Changes the hue of a given hsv color

    Arguments:
        color (tuple): the color in hsv format (360, 1, 1)
        hue (float): the new hue (value between 0 and 360)

    Returns:
        (tuple): the new hsv formatted color
    """
    if hue is None:
        return color
    return (hue, color[1], color[2])


def change_hsv_saturation(color: tuple, saturation: int) -> tuple:
    """
    Changes the saturation of a given hsv color

    Arguments:
        color (tuple): the color in hsv format (360, 1, 1)
        saturation (float): the new saturation (value between 0 and 1)

    Returns:
        (tuple): the new hsv formatted color
    """
    if saturation is None:
        return color
    return (color[0], saturation, color[2])


def change_hsv_value(color: tuple, value: int) -> tuple:
    """
    Changes the value of a given hsv color

    Arguments:
        color (tuple): the color in hsv format (360, 1, 1)
        value (float): the new value (value between 0 and 1)

    Returns:
        (tuple): the new hsv formatted color
    """
    if value is None:
        return color
    return (color[0], color[1], value)


def change_rgb_hue(color: tuple, hue: int) -> tuple:
    """
    Changes the hue of a given rgb color

    Arguments:
        color (tuple): the color in rgb format (255, 255, 255)
        hue (float): the new hue (value between 0 and 360)

    Returns:
        (tuple): the new rgb formatted color
    """
    if hue is None:
        return color
    hsv_color = rgb_to_hsv(color)
    hsv_color = (hue, hsv_color[1], hsv_color[2])
    return hsv_to_rgb(hsv_color)


def change_rgb_saturation(color: tuple, saturation: int) -> tuple:
    """
    Changes the saturation of a given rgb color

    Arguments:
        color (tuple): the color in rgb format (255, 255, 255)
        saturation (float): the new saturation (value between 0 and 1)

    Returns:
        (tuple): the new rgb formatted color
    """
    if saturation is None:
        return color
    hsv_color = rgb_to_hsv(color)
    hsv_color = (hsv_color[0], saturation, hsv_color[2])
    return hsv_to_rgb(hsv_color)


def change_rgb_value(color: tuple, value: int) -> tuple:
    """
    Changes the value of a given rgb color

    Arguments:
        color (tuple): the color in rgb format (255, 255, 255)
        value (float): the new value (value between 0 and 1)

    Returns:
        (tuple): the new rgb formatted color
    """
    if value is None:
        return color
    hsv_color = rgb_to_hsv(color)
    hsv_color = (hsv_color[0], hsv_color[1], value)
    return hsv_to_rgb(hsv_color)


def get_rgb_hue(color: tuple) -> int:
    """
    Gets the hue of an rgb color

    Arguments:
        color (tuple): the color in rgb format

    Returns:
        (int): the hue of the rgb color
    """
    hsv_color = rgb_to_hsv(color)
    return hsv_color[0]


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
    return rgb_to_hex(change_rgb_saturation(change_rgb_value(color, value), saturation))


def make_palette(colors: tuple, values: tuple, saturations: tuple) -> dict:
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
        new_colors[f"color{str(i + 1)}"] = modify_rgb_value_saturation(
            colors[i + 1], default_dark, color
        )
        new_colors[f"color{str(i + 9)}"] = modify_rgb_value_saturation(
            colors[i + 1], default_light, color
        )

    return new_colors
