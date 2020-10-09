import argparse
import sys
import os.path
import logging
import shutil
import random

from kadai import log
from kadai import config_handler
from kadai.config_handler import ConfigHandler
from kadai.utils import FileUtils
from kadai.themer import Themer

logger = log.setup_logger(__name__, log.defaultLoggingHandler(), level=logging.WARNING)

configHandler = ConfigHandler()
configHandler.save()
config = configHandler.get()

def get_args():
    """ Get the args parsed from the command line and does arg handling stuff """

    arg = argparse.ArgumentParser(description="Generate and switch wallpaper themes")

    arg.add_argument('-v', action='store_true',
        help='Verbose Logging')

    arg.add_argument("-g", action="store_true",
        help="generate themes")
    
    arg.add_argument("-i", metavar="\"path/to/dir\"",
        help="the input file")
    
    arg.add_argument("-p", action="store_true",
        help="Use last set theme")

    arg.add_argument('--override', action="store_true",
        help="Override exisiting themes")
    
    arg.add_argument("--clear", action="store_true",
        help="Clear all data relating to KADAI")

    arg.add_argument("--backend", metavar="name",
        help="vibrance/hue/k_means")

    arg.add_argument("--progress", action="store_true",
        help="Show progress of theme generation")

    arg.add_argument("--warranty", action="store_true",
        help="Show the programs warranty")

    arg.add_argument("--light", action="store_true",
        help="Enable light theme")

    return arg

def parse_args(parser):
    """
    Parses the arguments onto different actions

    Arguments:
        parser (idk) -- the argument parser
    """

    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    VERBOSE_MODE = True if args.v else False

    # Determine flags from config and cli
    engine_type = config_handler.compareFlagWithConfig(args.backend, config['engine'])
    show_progress = config_handler.compareFlagWithConfig(args.progress, config['progress'])
    enable_light_theme = config_handler.compareFlagWithConfig(args.light, config['light'])

    if args.warranty:
        print("""Copyright (C) 2020 slapelachie

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.""")
        exit(0)

    if args.i:
        themer = Themer(args.i, config['data_directory'])
        themer.setEngine(engine_type)
        themer.setOverride(args.override)
        themer.disableProgress(not show_progress)
        if enable_light_theme:
            themer.enableLightTheme()

        if args.g:
            themer.generate()
            sys.exit(0)
        else:
            # If the theme file does not exist generate it and then update to it
            try:
                themer.update()
            except FileUtils.noPreGenThemeError:
                themer.generate()
                themer.update()
            sys.exit(0)
    elif args.p:
        # Check if the cached image exists, if it does update to that
        last_image = os.path.join(config['data_directory'], "image")
        if(FileUtils.check_if_image(last_image)):
            themer = Themer(last_image, config['data_directory'])
            if enable_light_theme:
                themer.enableLightTheme()
            themer.update()
        else:
            logger.critical("Last image invalid or does not exist!")
            sys.exit(1)
    
    elif args.clear:
        clear = input("Are you sure you want to remove the cache relating to KADAI? [y/N] ").lower()
        if(clear == "y"):
            try:
                shutil.rmtree(config['cache_directory'])
            except:
                raise
            logger.info("Cleared KADAI cache folders")
        else:
            logger.info("Canceled clearing cache folders...")
    else:
        logger.critical("No file specified...")
        sys.exit(1)

def main():
    # Create required directories
    try:
        os.makedirs(config['cache_directory'], exist_ok=True)
        os.makedirs(config['data_directory'], exist_ok=True)
        os.makedirs(FileUtils.getConfigPath(), exist_ok=True)
    except:
        raise

    parser = get_args()
    parse_args(parser)

if __name__ == "__main__":
    main()

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