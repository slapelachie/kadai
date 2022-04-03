"""
Contains everything needed for theming

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
import os
import re
import logging
import json
import random
import errno
from io import TextIOWrapper
from typing import Dict, List
import tqdm
from PIL import Image

from kadai.utils import file_utils, color_utils
from kadai.config_handler import ConfigHandler
from kadai.engine import BaseEngine
from kadai import log


TMP_FILE = "/tmp/kadai-tmp.png"

logger = log.setup_logger(
    __name__ + ".default", log.defaultLoggingHandler(), level=logging.WARNING
)
tqdm_logger = log.setup_logger(
    __name__ + ".tqdm", log.TqdmLoggingHandler(), level=logging.WARNING
)

config_handler = ConfigHandler()
config = config_handler.get_config()

# pylint: disable=too-many-instance-attributes,too-many-public-methods
class Themer:
    """The themer class, sets up everything for theming"""

    def __init__(self, image_path: str, **kwargs):
        """
        The initialization for the themer class

        Arguments:
            image_path (str): the path to the image to be used for the theme
            **config (idk): the config to be used
            **override (bool): whether to override the output
            **run_hooks (bool): should the hooks be run after
            **display_progress (bool): should the progress be displayed
            **use_light_theme (bool): should a light theme be used
            **engine_name (str): the name of the engine to use
            **out_path (str): the path to export the theme to
            **cache_path (str): the path to cache to
            **user_template_path (str): the path to the users templates
            **user_hooks_path (str): the path to the users hooks
            **custom_theme_path (str): the path to the custom theme
        """
        self._image_path = image_path

        self._config = kwargs.get("config", config)
        self._override = kwargs.get("override", False)
        self._run_hooks = kwargs.get("run_hooks", True)
        self._display_progress = kwargs.get(
            "display_progress", self._config["progress"]
        )
        self._use_light_theme = kwargs.get("use_light_theme", self._config["light"])
        self._engine_name = kwargs.get("engine_name", self._config["engine"])
        self._out_path = kwargs.get("out_path", self._config["data_directory"])
        self._cache_path = kwargs.get("cache_path", self._config["cache_directory"])
        self._user_templates_path = kwargs.get(
            "user_template_path",
            os.path.join(file_utils.get_config_path(), "templates/"),
        )
        self._user_hooks_path = kwargs.get(
            "user_hooks_path", os.path.join(file_utils.get_config_path(), "hooks/")
        )

        self._custom_theme_path = kwargs.get(
            "custom_theme_path",
            self._config["custom_theme_path"]
            if self._config["use_custom_theme"]
            else None,
        )

        self._engine = get_engine(self._engine_name)
        self._theme_out_path = os.path.join(self._cache_path, "themes/")
        self._template_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "data/template.json"
        )

        os.makedirs(self._theme_out_path, exist_ok=True)

    def set_override(self, state: bool):
        """
        Updates the override

        Arguments:
            state (bool): the state to update to
        """
        self._override = state

    def get_override(self) -> bool:
        """
        Gets the override

        Returns:
            (bool): the state of the override
        """
        return self._override

    def set_run_hooks(self, state: bool):
        """
        Updates the run hooks state

        Arguments:
            state (bool): the state to update to
        """
        self._run_hooks = state

    def get_run_hooks(self) -> bool:
        """
        Gets the run hooks state

        Returns:
            (bool): the state of run hooks
        """
        return self._run_hooks

    def set_display_progress(self, state):
        """
        Sets the display progress state

        Arguments:
            state (bool): the state to update to
        """
        self._display_progress = state

    def get_display_progress(self) -> bool:
        """
        Gets the display progress state

        Returns:
            (bool): the display progress state
        """
        return self._display_progress

    def set_use_light_theme(self, state: bool):
        """
        Sets the use light theme state

        Arguments:
            state (bool): the state to update to
        """
        self._use_light_theme = state

    def get_use_light_theme(self) -> bool:
        """
        Gets the use light theme state

        Returns:
            (bool): the use light theme state
        """
        return self._use_light_theme

    def set_engine_name(self, engine_name: str):
        """
        Sets the name of the engine to be used

        Arguments:
            engine_name (str): the name of the engine to use
        """
        self._engine_name = engine_name
        self._engine = get_engine(engine_name)

    def get_engine_name(self) -> bool:
        """
        Gets the current engine name

        Returns:
            (bool): the name of the engine
        """
        return self._engine_name

    def set_out_path(self, path: str):
        """
        Sets the path to export the theme to

        Arguments:
            path (str): the path to export the theme to
        """
        self._out_path = path

    def get_out_path(self) -> str:
        """
        Gets the current export path

        Returns:
            (str): the current export path
        """
        return self._out_path

    def set_cache_path(self, path: str):
        """
        Sets the cache path

        Arguments:
            path (str): the cache path
        """
        self._cache_path = path
        self._theme_out_path = os.path.join(self._cache_path, "themes/")
        os.makedirs(self._theme_out_path, exist_ok=True)

    def get_cache_path(self) -> str:
        """
        Gets the current cache path

        Returns:
            (str): the cache path
        """

        return self._cache_path

    def set_user_template_path(self, path: str):
        """
        Sets the user template path

        Arguments:
            path (str): the user template path
        """
        self._user_templates_path = path

    def get_user_template_path(self) -> str:
        """
        Gets the user template path

        Returns:
            (str): the user template path
        """
        return self._user_templates_path

    def set_user_hooks_path(self, path: str):
        """
        Get the user hooks path


        Arguments:
            path (str): the user hooks path
        """
        self._user_hooks_path = path

    def get_user_hooks_path(self) -> str:
        """
        Gets the user hooks path

        Returns:
            (str): the user hooks path
        """
        return self._user_hooks_path

    def set_custom_theme_path(self, path: str):
        """
        Set the custom theme path

        Arguments:
            path (str): the path to the theme file
        """
        self._custom_theme_path = path

    def get_custom_theme_path(self) -> str:
        """
        Get the path to the custom theme file

        Returns:
            (str): the path to the custom theme file
        """

    def get_color_palette(self) -> Dict:
        """
        Gets the generated color palette depending on if the light theme or the
        dark theme are needed, fails if it does not exist

        The format of the returned pallete is as follows

        {
            "color0": "#ffffff",
            "color1": "#ffffff",
            ...
            "color15": "#ffffff"
        }

        Returns:
            (Dict): a dictionary containing all the colors
        """
        md5_hash = file_utils.md5_file(self._image_path)[:20]
        theme_out_file_path = os.path.join(
            self._theme_out_path, f"{md5_hash}-{self._engine_name}.json"
        )

        if not os.path.isfile(theme_out_file_path):
            raise file_utils.NoPreGenThemeError(
                "Theme file for this image does not exist!"
            )

        with open(theme_out_file_path, "r+", encoding="UTF-8") as json_data:
            theme_data = json.load(json_data)

        colors = theme_data["colors"]

        return colors["light"] if self._use_light_theme else colors["dark"]

    def generate(self):
        """Generates the theme"""
        path_image_names = [
            [i, f"{file_utils.md5_file(i)[:20]}-{self._engine_name}"]
            for i in file_utils.get_image_list(self._image_path)
        ]
        unprocessed_images = (
            path_image_names
            if self._override
            else get_non_generated(
                path_image_names,
                self._theme_out_path,
            )
        )

        if len(unprocessed_images) > 0:
            for i in tqdm.tqdm(
                range(len(unprocessed_images)),
                bar_format=log.bar_format,
                disable=self._display_progress,
            ):
                image = unprocessed_images[i][0]
                filename = unprocessed_images[i][1]
                out_file = os.path.join(self._theme_out_path, f"{filename}.json")

                create_tmp_image(image, TMP_FILE)

                color_engine = self._engine(TMP_FILE)
                dominant_color = color_utils.rgb_to_hex(
                    color_engine.get_dominant_color()
                )

                tqdm_logger.log(
                    15,
                    "[%s/%s] Generating theme for {%s}...",
                    str(i + 1),
                    str(len(unprocessed_images)),
                    image,
                )

                if not self._custom_theme_path:
                    palette = color_engine.get_palette()
                    create_template_from_palette(
                        palette, dominant_color, str(image), out_file
                    )
                else:
                    create_template_from_custom_palette(
                        self._custom_theme_path, dominant_color, str(image), out_file
                    )
        else:
            logger.info("No themes to generate.")

    def update(self):
        """Updates the current theme"""
        if os.path.isdir(self._image_path):
            images = file_utils.get_image_list(self._image_path)
            random.shuffle(images)
            self._image_path = images[0]
        elif not os.path.isfile(self._image_path):
            raise file_utils.NoPreGenThemeError("Provided file is not recognised!")

        md5_hash = file_utils.md5_file(self._image_path)[:20]
        theme_out_file_path = os.path.join(
            self._theme_out_path, f"{md5_hash}-{self._engine_name}.json"
        )

        if not os.path.isfile(theme_out_file_path):
            raise file_utils.NoPreGenThemeError(
                "Theme file for this image does not exist!"
            )

        with open(theme_out_file_path, "r+", encoding="UTF-8") as json_data:
            theme_data = json.load(json_data)

        colors = theme_data["colors"]
        primary_color = theme_data["primary"]
        wallpaper = theme_data["wallpaper"]

        theme_colors = colors["light"] if self._use_light_theme else colors["dark"]

        try:
            templates = get_template_files(self._user_templates_path)

            for template in templates:
                template_path = os.path.join(self._user_templates_path, template)
                out_file = os.path.join(self._out_path, template[:-5])
                create_file_from_template(
                    template_path, out_file, theme_colors, primary_color
                )
        except FileNotFoundError:
            tqdm_logger.warning("No templates files found...")

        # Link wallpaper to cache folder
        symlink_image_path(wallpaper, self._out_path)

        # Run external scripts
        if self._run_hooks:
            file_utils.run_hooks(
                use_light_theme=self._use_light_theme,
                hooks_directory=self._user_hooks_path,
            )


def get_engine(engine_name: str) -> BaseEngine:
    """
    Get the engine from the name given

    Arguments:
        engine_name (str): the name of the engine

    Returns:
        (BaseEngine): the engine class
    """
    # pylint: disable=import-outside-toplevel
    if engine_name == "hue":
        from kadai.engine import HueEngine

        return HueEngine

    if engine_name == "pastel":
        from kadai.engine import PastelEngine

        return PastelEngine
    if engine_name == "pastel_hue":
        from kadai.engine import PastelHueEngine

        return PastelHueEngine

    from kadai.engine import VibranceEngine

    return VibranceEngine


def get_template_files(template_directory: str) -> List[str]:
    """
    Get all templates in the templates folder

    Arguments:
        template_directory (str): the directory containing the templates

    Returns:
        (List[str]): a list containing all the templates within the directory
    """
    return [f for f in os.listdir(template_directory) if re.match(r".*\.base$", f)]


def get_non_generated(image_paths: List[str], theme_directory: str) -> List[str]:
    """
    Get the files that have not been generated by the themer

    Arguments:
        image_paths (List[str]): a list containing the paths of images
        theme_directory (str): the path in which the themes are stored

    Returns:
        (List[str]): a list containing images that have not had their themes
                     generated
    """
    ungenerated_images = []
    theme_directory = os.path.expanduser(theme_directory)
    for image_path in image_paths:
        filename = image_path[1]

        matched_files = [
            os.path.join(theme_directory, x.name)
            for x in os.scandir(theme_directory)
            if filename in x.name
        ]

        if len(matched_files) == 0:
            ungenerated_images.append(image_path)

    return ungenerated_images


def clear_write_data_to_file(file_path: str, data: TextIOWrapper):
    """
    Clear the data in a file and write data to it

    Arguments:
        file_path (str): the path to the file
        data (io.TextIOWrapper): the data to write to the file
    """
    if os.path.isfile(file_path):
        with open(os.path.expanduser(file_path), "w", encoding="UTF-8"):
            pass

    with open(os.path.expanduser(file_path), "a", encoding="UTF-8") as file:
        file.write(data)


def clear_write_json_to_file(file_path: str, json_data):
    """
    Clear the data in a file and write json data to it

    Arguments:
        file_path (str): the path to the file
        json_data (idk): the json data to write
    """
    if os.path.isfile(file_path):
        with open(os.path.expanduser(file_path), "w", encoding="UTF-8"):
            pass

    with open(os.path.expanduser(file_path), "wb") as file:
        file.write(
            json.dumps(json_data, indent=4, separators=(",", ": ")).encode("utf-8")
        )


def create_template_from_palette(
    palette: Dict, dominant_color: str, image_path: str, out_path: str
):
    """
    Create and write the file from a template using a palette

    Arguments:
        palette (Dict): the color palette to write
        dominant_color (str): the dominant color generated in hex
        image_path (str): the path to the image used in the theme
        out_path (str): the path the file will be exported to
    """
    file_contents = {}
    file_contents["colors"] = palette
    file_contents["wallpaper"] = image_path
    file_contents["primary"] = dominant_color

    clear_write_json_to_file(out_path, file_contents)


def create_template_from_custom_palette(
    custom_theme_path: str, dominant_color: str, image_path: str, out_path: str
):
    custom_theme_data = {}
    with open(custom_theme_path, "r+", encoding="UTF-8") as json_data:
        custom_theme_data = json.load(json_data)

    create_template_from_palette(
        custom_theme_data, dominant_color, image_path, out_path
    )


def create_tmp_image(image_path: str, out_path: str):
    """
    Create a smaller version of the image so color extraction does not take as long

    Arguments:
        image_path (str): the path to the image
        out_path (str): where to export the new image to
    """
    image = Image.open(image_path).resize((100, 50), Image.Resampling.NEAREST).convert("RGB")
    image.save(out_path)


def modify_file_with_template(file_data: str, colors: Dict, primary_color: str) -> str:
    """
    Modify the template with data to replace

    Arguments:
        file_data (str): the template file data
        colors (Dict): a dictionary containing all the colors
        primary_color (str): the main color to be used

    Returns:
        (str): the modified file data
    """
    for i in range(len(colors)):
        file_data = file_data.replace(
            "[color" + str(i) + "]", str(colors["color" + str(i)])
        )

    file_data = file_data.replace("[background]", str(colors["color0"]))
    file_data = file_data.replace("[background_light]", str(colors["color8"]))
    file_data = file_data.replace("[foreground]", str(colors["color15"]))
    file_data = file_data.replace("[foreground_dark]", str(colors["color7"]))
    file_data = file_data.replace("[primary]", str(primary_color))

    return file_data


def symlink_image_path(image_path: str, folder_path: str):
    """
    symlink the given image to a path

    Arguments:
        image_path (str): the path to the image to be linked
        folder_path (str): the path to the folder to symlink to
    """
    image_symlink = os.path.join(folder_path, "image")

    try:
        os.symlink(image_path, image_symlink)
    except OSError as exception:
        if exception.errno == errno.EEXIST:
            os.remove(image_symlink)
            os.symlink(image_path, image_symlink)
        else:
            raise exception


def create_file_from_template(
    template_file_path: str, out_file: str, colors: Dict, primary_color: str
):
    """
    Create a file given a template and substitute colors within, export to the
    out file

    Arguments:
        template_path (str): the path to the template file
        out_file (str): where to export the new file
        colors (Dict): the colors to use
        primary_color (str): the primary color
    """
    with open(template_file_path, "r+", encoding="UTF-8") as template_file:
        file_data = template_file.read()
        file_data = modify_file_with_template(file_data, colors, primary_color)

        clear_write_data_to_file(out_file, file_data)
