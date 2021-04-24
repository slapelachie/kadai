import os
import re
import tqdm
import logging
import json
import random
import errno
from colorthief import ColorThief
from PIL import Image

from kadai.utils import file_utils, color_utils
from kadai.config_handler import ConfigHandler
from kadai.engine import BaseEngine
from kadai import log

logger = log.setup_logger(
    __name__ + ".default", log.defaultLoggingHandler(), level=logging.WARNING
)
tqdm_logger = log.setup_logger(
    __name__ + ".tqdm", log.TqdmLoggingHandler(), level=logging.WARNING
)

configHandler = ConfigHandler()
config = configHandler.get()


class Themer:
    def __init__(self, image_path, out_path=config["data_directory"], config=config):
        self.config = config
        self.image_path = image_path
        self.out_path = out_path
        self.override = False
        self.run_hooks = True
        self.engine_name = self.config["engine"]
        self.engine = get_engine(self.engine_name)
        self.cache_path = self.config["cache_directory"]
        self.theme_out_path = os.path.join(self.cache_path, "themes/")
        self.template_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "data/template.json"
        )
        self.user_templates_path = os.path.join(
            file_utils.get_config_path(), "templates/"
        )
        self.user_hooks_path = os.path.join(file_utils.get_config_path(), "hooks/")
        self.progress = self.config["progress"]
        self.light_theme = self.config["light"]

        file_utils.ensure_dir_exists(self.theme_out_path)

    def set_image_path(self, path):
        self.image_path = path

    def set_out_path(self, path):
        self.out_path = path

    def set_cache_path(self, path):
        self.cache_path = path
        self.theme_out_path = os.path.join(self.cache_path, "themes/")
        file_utils.ensure_dir_exists(self.theme_out_path)

    def set_engine(self, engine_name):
        self.engine_name = engine_name
        self.engine = get_engine(engine_name)

    def set_override(self, state):
        self.override = state

    def set_user_template_path(self, path):
        self.user_templates_path = path

    def set_user_hooks_path(self, path):
        self.user_hooks_path = path

    def set_run_hooks(self, condition):
        self.run_hooks = condition

    def disable_progress(self, condition):
        self.progress = condition

    def enable_light_theme(self):
        self.light_theme = True

    def get_color_palette(self):
        theme_colors = None
        md5_hash = file_utils.md5_file(self.image_path)[:20]

        if not os.path.isfile(
            os.path.join(
                self.theme_out_path, "{}-{}.json".format(md5_hash, self.engine_name)
            )
        ):
            raise file_utils.noPreGenThemeError(
                "Theme file for this image does not exist!"
            )

        with open(
            os.path.join(
                self.theme_out_path, "{}-{}.json".format(md5_hash, self.engine_name)
            )
        ) as json_data:
            theme_data = json.load(json_data)

        colors = theme_data["colors"]

        if self.light_theme:
            theme_colors = colors["light"]
        else:
            theme_colors = colors["dark"]

        return theme_colors

    def generate(self):
        tmp_file = "/tmp/kadai-tmp.png"

        image_path_name = [
            [i, "{}-{}".format(file_utils.md5_file(i)[:20], self.engine_name)]
            for i in file_utils.get_image_list(self.image_path)
        ]
        unprocessed_images = (
            image_path_name
            if self.override
            else get_non_generated(
                image_path_name,
                self.theme_out_path,
            )
        )

        if len(unprocessed_images) > 0:
            for i in tqdm.tqdm(
                range(len(unprocessed_images)),
                bar_format=log.bar_format,
                disable=self.progress,
            ):
                image = unprocessed_images[i][0]
                filename = unprocessed_images[i][1]
                out_file = os.path.join(self.theme_out_path, "{}.json".format(filename))

                create_tmp_image(image, tmp_file)

                color_engine = self.engine(tmp_file)
                palette = color_engine.get_palette()
                dominant_color = color_utils.rgb_to_hex(
                    color_engine.get_dominant_color()
                )

                tqdm_logger.log(
                    15,
                    "[{}/{}] Generating theme for {}...".format(
                        str(i + 1), str(len(unprocessed_images)), image
                    ),
                )

                create_template_from_palette(
                    palette, dominant_color, str(image), out_file
                )
                # with open(self.template_path) as template_file:
        else:
            logger.info("No themes to generate.")

    def update(self):
        if os.path.isdir(self.image_path):
            images = file_utils.get_image_list(self.image_path)
            random.shuffle(images)
            self.image_path = images[0]
        elif not os.path.isfile(self.image_path):
            raise file_utils.noPreGenThemeError("Provided file is not recognised!")

        md5_hash = file_utils.md5_file(self.image_path)[:20]

        if not os.path.isfile(
            os.path.join(
                self.theme_out_path, "{}-{}.json".format(md5_hash, self.engine_name)
            )
        ):
            raise file_utils.noPreGenThemeError(
                "Theme file for this image does not exist!"
            )

        with open(
            os.path.join(
                self.theme_out_path, "{}-{}.json".format(md5_hash, self.engine_name)
            )
        ) as json_data:
            theme_data = json.load(json_data)

        colors = theme_data["colors"]
        primary_color = theme_data["primary"]
        wallpaper = theme_data["wallpaper"]

        if self.light_theme:
            theme_colors = colors["light"]
        else:
            theme_colors = colors["dark"]

        try:
            templates = get_template_files(self.user_templates_path)

            for template in templates:
                template_path = os.path.join(self.user_templates_path, template)
                out_file = os.path.join(self.out_path, template[:-5])
                create_file_from_template(
                    template_path, out_file, theme_colors, primary_color
                )
        except FileNotFoundError:
            tqdm_logger.warn("No templates files found...")

        # Link wallpaper to cache folder
        link_wallpaper_path(wallpaper, self.out_path)

        # Run external scripts
        if self.run_hooks:
            file_utils.run_hooks(
                light_theme=self.light_theme, hooks_dir=self.user_hooks_path
            )


def get_engine(engine_name: str) -> BaseEngine:
    if engine_name == "hue":
        from kadai.engine import HueEngine

        return HueEngine
    elif engine_name == "pastel":
        from kadai.engine import PastelEngine

        return PastelEngine
    elif engine_name == "pastel_hue":
        from kadai.engine import PastelHueEngine

        return PastelHueEngine
    elif engine_name == "k_means":
        from kadai.engine import kMeansEngine

        return kMeansEngine
    else:
        from kadai.engine import VibranceEngine

        return VibranceEngine


def get_avaliable_engines():
    engines = []
    try:
        from kadai.engine import HueEngine

        engines.append("hue")
    except:
        pass

    try:
        from kadai.engine import VibranceEngine

        engines.append("vibrance")
    except:
        pass

    try:
        from kadai.engine import kMeansEngine

        engines.append("k_means")
    except:
        pass

    return engines


def get_template_files(template_dir):
    # Get all templates in the templates folder
    try:
        templates = [f for f in os.listdir(template_dir) if re.match(r".*\.base$", f)]
    except FileNotFoundError:
        raise FileNotFoundError

    return templates


def get_non_generated(images, theme_dir):
    ungenerated_images = []
    theme_dir = os.path.expanduser(theme_dir)
    for i in range(len(images)):
        filename = images[i][1]

        if (
            len(
                [
                    os.path.join(theme_dir, x.name)
                    for x in os.scandir(theme_dir)
                    if filename in x.name
                ]
            )
            == 0
        ):
            ungenerated_images.append(images[i])

    return ungenerated_images


def clear_write_data_to_file(file_path, data):
    if os.path.isfile(file_path):
        open(os.path.expanduser(file_path), "w").close()
    with open(os.path.expanduser(file_path), "a") as file:
        file.write(data)


def clear_write_json_to_file(file_path, json_data):
    if os.path.isfile(file_path):
        open(os.path.expanduser(file_path), "w").close()
    with open(os.path.expanduser(file_path), "wb") as file:
        file.write(
            json.dumps(json_data, indent=4, separators=(",", ": ")).encode("utf-8")
        )


def create_template_from_palette(palette, dominant_color, image_path, out_path):
    file_contents = {}
    file_contents["colors"] = palette
    file_contents["wallpaper"] = image_path
    file_contents["primary"] = dominant_color

    clear_write_json_to_file(out_path, file_contents)


def create_tmp_image(image, path):
    img = Image.open(image)
    image_out = img.resize((100, 50), Image.NEAREST).convert("RGB")
    image_out.save(path)


def modify_file_with_template(filedata, colors, primary_color):
    # Change placeholder values
    for i in range(len(colors)):
        filedata = filedata.replace(
            "[color" + str(i) + "]", str(colors["color" + str(i)])
        )

    filedata = filedata.replace("[background]", str(colors["color0"]))
    filedata = filedata.replace("[background_light]", str(colors["color8"]))
    filedata = filedata.replace("[foreground]", str(colors["color15"]))
    filedata = filedata.replace("[foreground_dark]", str(colors["color7"]))
    filedata = filedata.replace("[primary]", str(primary_color))

    return filedata


def link_wallpaper_path(wallpaper, folder_path):
    image_symlink = os.path.join(folder_path, "image")

    try:
        os.symlink(wallpaper, image_symlink)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(image_symlink)
            os.symlink(wallpaper, image_symlink)
        else:
            raise e


def create_file_from_template(template_path, out_file, colors, primary_color):
    with open(template_path) as template_file:
        filedata = template_file.read()
        filedata = modify_file_with_template(filedata, colors, primary_color)

        clear_write_data_to_file(out_file, filedata)


"""
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