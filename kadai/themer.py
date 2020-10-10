import os
import re
import tqdm
import logging
import json
import random
import errno
from colorthief import ColorThief
from PIL import Image

from kadai.utils import FileUtils,ColorUtils
from kadai.config_handler import ConfigHandler
from kadai import log

logger = log.setup_logger(__name__+'.default', log.defaultLoggingHandler(), level=logging.WARNING)
tqdm_logger = log.setup_logger(__name__+'.tqdm', log.TqdmLoggingHandler(), level=logging.WARNING)

configHandler = ConfigHandler()
config = configHandler.get()

class Themer():
    def __init__(self, image_path, out_path):
        self.image_path = image_path
        self.out_path = out_path
        self.cache_path = config['cache_directory']
        self.override = False
        self.run_hooks = True
        self.engine_name = 'vibrance'
        self.engine = getEngine(self.engine_name)
        self.theme_out_path = os.path.join(self.cache_path, 'themes/')
        self.template_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
            "data/template.json")
        self.user_templates_path = os.path.join(FileUtils.getConfigPath(), 'templates/')
        self.disable_progress = True
        self.light_theme = False

        FileUtils.ensure_dir_exists(self.theme_out_path)

    def setImagePath(self, path):
        self.image_path = path

    def setOutPath(self, path):
        self.out_path = path

    def setCachePath(self, path):
        self.cache_path = path
        self.theme_out_path = os.path.join(self.cache_path, 'themes/')
        FileUtils.ensure_dir_exists(self.theme_out_path)

    def setEngine(self, engine_name):
        self.engine_name = engine_name
        self.engine = getEngine(engine_name)

    def setOverride(self, state):
        self.override = state
    
    def setUserTemplatePath(self, path):
        self.user_templates_path = path
    
    def setRunHooks(self, condition):
        self.run_hooks = condition

    def disableProgress(self, condition):
        self.disable_progress = condition

    def enableLightTheme(self):
        self.light_theme = True
    
    def generate(self):
        tmp_file = "/tmp/kadai-tmp.png"

        image_path_md5 = [[i, FileUtils.md5_file(i)[:20]] for i in FileUtils.get_image_list(self.image_path)]
        unprocessed_images = image_path_md5 if self.override else get_non_generated(image_path_md5, self.theme_out_path)

        if len(unprocessed_images) > 0:
            for i in tqdm.tqdm(range(len(unprocessed_images)), bar_format=log.bar_format, disable=self.disable_progress):
                image = unprocessed_images[i][0]
                md5_hash = unprocessed_images[i][1]
                out_file = os.path.join(self.theme_out_path, md5_hash + '.json')
            
                create_tmp_image(image, tmp_file)

                colors = self.engine(tmp_file).generate()
                pallete = createValueColorPallete(colors)

                tqdm_logger.log(15, "[" + str(i+1) + "/" + str(len(unprocessed_images)) + "] Generating theme for " + image + "...")
            
                createTemplateFromPallete(pallete, str(image), out_file)
                #with open(self.template_path) as template_file:
        else:
            logger.info("No themes to generate.")
        
    def update(self):
        if os.path.isdir(self.image_path):
            images = FileUtils.get_image_list(self.image_path)
            random.shuffle(images)
            self.image_path = images[0]
        elif not os.path.isfile(self.image_path):
            raise FileUtils.noPreGenThemeError("Provided file is not recognised!")
        
        md5_hash = FileUtils.md5_file(self.image_path)[:20]

        if not os.path.isfile(os.path.join(self.theme_out_path, md5_hash+".json")):
            raise FileUtils.noPreGenThemeError("Theme file for this image does not exist!")

        with open(os.path.join(self.theme_out_path, md5_hash + ".json")) as json_data:
            theme_data = json.load(json_data)

        colors = theme_data['colors']
        primary_color = theme_data['primary']
        wallpaper = theme_data['wallpaper']

        if self.light_theme:
            theme_colors = makeLightThemeFromColors(colors)
        else:
            theme_colors = makeDarkThemeFromColors(colors)

        templates = get_template_files(self.user_templates_path)

        for template in templates:
            template_path = os.path.join(self.user_templates_path, template)
            out_file = os.path.join(self.out_path, template[:-5])
            createFileFromTemplate(template_path, out_file, theme_colors, primary_color)
        
        # Link wallpaper to cache folder
        linkWallpaperPathInFolder(wallpaper, self.out_path)

        # Run external scripts
        if self.run_hooks:
            FileUtils.run_hooks(light_theme=self.light_theme)

def getEngine(engine_name):
    if engine_name == "hue":
        from kadai.engine import HueEngine
        return HueEngine
    elif engine_name == "k_means":
        from kadai.engine import kMeansEngine
        return kMeansEngine
    else:
        from kadai.engine import VibranceEngine
        return VibranceEngine

def createValueColorPallete(colors):
    values = [0.1, 0.3, 0.5, 0.7, 0.9]
    pallete = {}
    for i in range(len(colors)):
        color_value_dictionary = createValueSpreadDictionary(values, colors[i])
        pallete['color{}'.format(i)] = color_value_dictionary
    return pallete

def createValueSpreadDictionary(values, color):
    pallete = {}
    for value in values:
        pallete[str(value)] =  ColorUtils.rgb_to_hex(ColorUtils.changeValueFromRGB(color, value))
    return pallete

def get_template_files(template_dir):
    # Get all templates in the templates folder
    templates = [f for f in os.listdir(template_dir)
        if re.match(r'.*\.base$', f)]

    return templates

def get_non_generated(images, theme_dir):
    ungenerated_images = []
    theme_dir = os.path.expanduser(theme_dir)
    for i in range(len(images)):
        md5_hash = images[i][1]

        if len([os.path.join(theme_dir, x.name) for x in os.scandir(theme_dir)\
            if md5_hash in x.name]) == 0:
            ungenerated_images.append(images[i])

    return ungenerated_images

def clearAndWriteDataToFile(file_path, data):
    if os.path.isfile(file_path):
        open(os.path.expanduser(file_path), 'w').close()
    with open(os.path.expanduser(file_path), 'a') as file:
        file.write(data)

def clearAndWriteJsonToFile(file_path, json_data):
    if os.path.isfile(file_path):
        open(os.path.expanduser(file_path), 'w').close()
    with open(os.path.expanduser(file_path), 'wb') as file:
        file.write(json.dumps(json_data,
            indent=4, separators=(',',': ')).encode('utf-8'))

def createTemplateFromPallete(pallete, image_path, out_path):
    file_contents = {}
    domiant_color = getDominantColorFromImage(image_path)
    file_contents['colors'] = pallete
    file_contents['wallpaper'] = image_path
    file_contents['primary'] = domiant_color

    clearAndWriteJsonToFile(out_path, file_contents)

def create_tmp_image(image, path):
    img = Image.open(image)
    image_out = img.resize((100,50), Image.NEAREST).convert('RGB')
    image_out.save(path)

def modifyFiledataWithTemplate(filedata, colors, primary_color):
    # Change placeholder values
    for i in range(len(colors)):
        filedata = filedata.replace("[color" + str(i) + "]", str(colors['color'+str(i)]))

    filedata = filedata.replace("[background]", str(colors['color0']))
    filedata = filedata.replace("[background_light]", str(colors['color8']))
    filedata = filedata.replace("[foreground]", str(colors['color15']))
    filedata = filedata.replace("[foreground_dark]", str(colors['color7']))
    filedata = filedata.replace("[primary]", str(primary_color))

    return filedata

def linkWallpaperPathInFolder(wallpaper, folder_path):
    image_symlink = os.path.join(folder_path, 'image')

    try:
        os.symlink(wallpaper, image_symlink)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(image_symlink)
            os.symlink(wallpaper, image_symlink)
        else:
            raise e

def getDominantColorFromImage(image_path):
    tmp_image_path = '/tmp/kadai-tmp.png'
    create_tmp_image(image_path, tmp_image_path)
    color_cmd = ColorThief(tmp_image_path).get_palette
    raw_colors = color_cmd(color_count=2, quality=3)
    return ColorUtils.rgb_to_hex(ColorUtils.hsv_to_rgb(ColorUtils.changeHsvValue(ColorUtils.rgb_to_hsv(raw_colors[0]), 0.6)))

def createFileFromTemplate(template_path, out_file, colors, primary_color):
    with open(template_path) as template_file:
        filedata = template_file.read()
        filedata = modifyFiledataWithTemplate(filedata, colors, primary_color)

        clearAndWriteDataToFile(out_file, filedata)

def makeLightThemeFromColors(colors):
    new_colors = {}
    new_colors['color0'] = ColorUtils.rgb_to_hex(ColorUtils.changeSaturationFromRGB(ColorUtils.hex_to_rgb(colors['color0']['0.9']), 0.05))
    new_colors['color7'] = ColorUtils.rgb_to_hex(ColorUtils.changeSaturationFromRGB(ColorUtils.hex_to_rgb(colors['color0']['0.3']), 0.2))
    new_colors['color8'] = ColorUtils.rgb_to_hex(ColorUtils.changeSaturationFromRGB(ColorUtils.hex_to_rgb(colors['color0']['0.7']), 0.05))
    new_colors['color15'] = ColorUtils.rgb_to_hex(ColorUtils.changeSaturationFromRGB(ColorUtils.hex_to_rgb(colors['color0']['0.1']), 0.2))
    for i in range(6):
        new_colors['color{}'.format(str(i+1))] = colors['color{}'.format(str(1+i))]['0.5']
        new_colors['color{}'.format(str(i+9))] = colors['color{}'.format(str(1+i))]['0.3']
    return new_colors

def makeDarkThemeFromColors(colors):
    new_colors = {}
    new_colors['color0'] = ColorUtils.rgb_to_hex(ColorUtils.changeSaturationFromRGB(ColorUtils.hex_to_rgb(colors['color0']['0.1']), 0.2))
    new_colors['color7'] = ColorUtils.rgb_to_hex(ColorUtils.changeSaturationFromRGB(ColorUtils.hex_to_rgb(colors['color0']['0.7']), 0.05))
    new_colors['color8'] = ColorUtils.rgb_to_hex(ColorUtils.changeSaturationFromRGB(ColorUtils.hex_to_rgb(colors['color0']['0.3']), 0.2))
    new_colors['color15'] = ColorUtils.rgb_to_hex(ColorUtils.changeSaturationFromRGB(ColorUtils.hex_to_rgb(colors['color0']['0.9']), 0.05))
    for i in range(6):
        new_colors['color{}'.format(str(i+1))] = colors['color{}'.format(str(1+i))]['0.7']
        new_colors['color{}'.format(str(i+9))] = colors['color{}'.format(str(1+i))]['0.9']
    return new_colors

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