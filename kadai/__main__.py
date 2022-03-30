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

import argparse
import sys
import os.path
import logging
import shutil

from kadai import log
from kadai.config_handler import ConfigHandler
from kadai.utils import file_utils
from kadai.themer import Themer

WARRANTY = """Copyright (C) 2021 slapelachie

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details."""


class InvalidLastImage(Exception):
    """Raised when the last image used does not exist or is invalid"""


def get_args():
    """Get the args parsed from the command line and does arg handling stuff"""

    arg = argparse.ArgumentParser(description="Generate and switch wallpaper themes")

    arg.add_argument("-v", "--verbose", action="store_true", help="Verbose Logging")
    arg.add_argument("-g", "--generate", action="store_true", help="generate themes")
    arg.add_argument("-i", "--input", metavar='"path/to/dir"', help="the input file")
    arg.add_argument("-p", "--preserve", action="store_true", help="Use last set theme")
    arg.add_argument(
        "-t", "--theme", metavar='"path/to/dir"', help="path to custom theme"
    )
    arg.add_argument(
        "-c",
        "--config",
        metavar='"path/to/config"',
        help="Custom config file at a different location",
    )
    arg.add_argument(
        "--override", action="store_true", help="Override exisiting themes"
    )
    arg.add_argument(
        "--clear", action="store_true", help="Clear all data relating to KADAI"
    )
    arg.add_argument("--backend", metavar="name", help="vibrance/hue/pastel/pastel_hue")
    arg.add_argument(
        "--progress", action="store_true", help="Show progress of theme generation"
    )
    arg.add_argument(
        "--warranty", action="store_true", help="Show the programs warranty"
    )
    arg.add_argument("--light", action="store_true", help="Enable light theme")

    return arg


# pylint: disable=too-many-branches
def parse_args(parser: argparse.ArgumentParser, config_handler: ConfigHandler):
    """
    Arguments are parsed here

    Arguments:
        parser (argparse.ArgumentParser): the parser object
        config_handler (kadai.ConfigHandler): the config handler
    """
    args = parser.parse_args()
    config = config_handler.get_config()
    logger = log.setup_logger(
        __name__, log.defaultLoggingHandler(), level=logging.WARNING
    )

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    if args.warranty:
        print(WARRANTY)
        sys.exit(0)

    if args.clear:
        clear = input(
            "Are you sure you want to remove the cache relating to KADAI? [y/N] "
        ).lower()
        if clear == "y":
            shutil.rmtree(config["cache_directory"])
            logger.info("Cleared KADAI cache folders")
        else:
            logger.info("Canceled clearing cache folders...")

        sys.exit(0)

    if args.config:
        config_handler.load_config(args.config)
        config = config_handler.get_config()

    if args.input:
        themer = Themer(
            args.input,
            config=config,
        )

        if args.override:
            themer.set_override(args.override)

        if args.backend:
            themer.set_engine_name(args.backend)

        if args.progress:
            themer.set_display_progress(args.progress)

        if args.light:
            themer.set_use_light_theme(args.light)

        if args.theme:
            themer.set_custom_theme_path(args.theme)

        if args.generate:
            themer.generate()
        else:
            update_theme(themer)

    elif args.preserve:
        last_image = os.path.join(config["data_directory"], "image")

        if file_utils.check_if_image(last_image):
            themer = Themer(
                os.readlink(last_image),
                config=config,
            )

            if args.override:
                themer.set_override(args.override)

            if args.backend:
                themer.set_engine_name(args.backend)

            if args.progress:
                themer.set_display_progress(args.progress)

            if args.light:
                themer.set_use_light_theme(args.light)

            update_theme(themer)
        else:
            logger.critical("Last image invalid or does not exist!")
            sys.exit(1)

    else:
        logger.critical("No options specified. Exiting...")
        sys.exit(1)


def update_theme(themer: Themer):
    """
    Updates the theme, if the theme was not generate it, do so

    Arguments:
        themer (kadai.Themer): the themer to update from
    """
    try:
        themer.update()
    except file_utils.NoPreGenThemeError:
        themer.generate()
        themer.update()


def main():
    """The main function that gets called"""
    config_object = ConfigHandler()
    config_object.save_config()
    config = config_object.get_config()

    # Create required directories
    os.makedirs(config["cache_directory"], exist_ok=True)
    os.makedirs(config["data_directory"], exist_ok=True)
    os.makedirs(file_utils.get_config_path(), exist_ok=True)

    parser = get_args()
    parse_args(parser, config_object)


if __name__ == "__main__":
    main()
