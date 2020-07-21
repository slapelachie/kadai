import os
import re
import tqdm
import logging
import json
import random
from PIL import Image

from kadai.utils import FileUtils
from kadai.settings import CONFIG_PATH
from kadai import log

logger = log.setup_logger(__name__+'.default', logging.WARNING, log.defaultLoggingHandler())
tqdm_logger = log.setup_logger(__name__+'.tqdm', logging.WARNING, log.TqdmLoggingHandler())

class Themer():
    def __init__(self, image_path, out_path):
        self.image_path = image_path
        self.out_path = out_path
        self.override = False
        self.run_post_scripts = True
        self.engine_name = 'vibrance'
        self.engine = getEngine(self.engine_name)
        self.theme_out_path = os.path.join(out_path, 'themes/')
        self.template_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
            "../data/template.json")
        self.user_templates_path = os.path.join(CONFIG_PATH, 'templates/')
        self.disable_progress = True

        FileUtils.ensure_dir_exists(self.theme_out_path)

    def setImagePath(self, path):
        self.image_path = path

    def setOutPath(self, path):
        self.out_path = path

    def setEngine(self, engine_name):
        self.engine_name = engine_name
        self.engine = getEngine(engine_name)

    def setOverride(self, state):
        self.override = state
    
    def setUserTemplatePath(self, path):
        self.user_templates_path = path
    
    def setRunPostScripts(self, condition):
        self.run_post_scripts = condition

    def disableProgress(self, condition):
        self.disable_progress = condition
    
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

                tqdm_logger.log(15, "[" + str(i+1) + "/" + str(len(unprocessed_images)) + "] Generating theme for " + image + "...")
            
                with open(self.template_path) as template_file:
                    create_file_from_template(template_file, str(image), colors, out_file)
        else:
            logger.info("No themes to generate.")
        
    def update(self):
        if os.path.isdir(self.image_path):
            images = FileUtils.get_image_list(self.image_path)
            random.shuffle(images)
            self.image_path = images[0]
        elif not os.path.isfile(self.image_path):
            print("err")
            exit(1)
        
        md5_hash = FileUtils.md5_file(self.image_path)[:20]

        if not os.path.isfile(os.path.join(self.theme_out_path, md5_hash+".json")):
            raise FileUtils.noPreGenThemeError("Theme file for this image does not exist!")

        with open(os.path.join(self.theme_out_path, md5_hash + ".json")) as json_data:
            theme_data = json.load(json_data)

        colors = theme_data['colors']
        wallpaper = theme_data['wallpaper']

        templates = get_template_files(self.user_templates_path)

        for template in templates:
            template_path = os.path.join(self.user_templates_path, template)
            out_file = os.path.join(self.out_path, template[:-5])
            with open(template_path) as template_file:
                filedata = template_file.read()
                filedata = modifyFiledataWithTemplate(filedata, colors)

                if os.path.isfile(out_file):
                    open(os.path.expanduser(out_file), 'w').close()
                with open(os.path.expanduser(out_file), 'a') as file:
                    file.write(filedata)

        
        # Link wallpaper to cache folder
        linkWallpaperToFolder(wallpaper, self.out_path)
        # Run external scripts
        if self.run_post_scripts:
            FileUtils.run_post_scripts()

def getEngine(engine_name):
    if engine_name == "hue":
        from kadai.engine import HueEngine
        return HueEngine
    else:
        from kadai.engine import VibranceEngine
        return VibranceEngine

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

def clear_and_write_data_to_file(file_path, data):
    if os.path.isfile(file_path):
        open(os.path.expanduser(file_path), 'w').close()
    with open(os.path.expanduser(file_path), 'a') as file:
        file.write(data)

def create_file_from_template(template_file, image_path, colors, out_path):
    filedata = template_file.read()

    # Change placeholder values
    filedata = filedata.replace("[wallpaper]", image_path)
    for i in range(len(colors)):
        filedata = filedata.replace("[color" + str(i) + "]", str(colors[i]))
    
    clear_and_write_data_to_file(out_path, filedata)

def create_tmp_image(image, path):
    img = Image.open(image)
    image_out = img.resize((150,75), Image.NEAREST).convert('RGB')
    image_out.save(path)

def modifyFiledataWithTemplate(filedata, colors):
    # Change placeholder values
    for i in range(len(colors)):
        filedata = filedata.replace("[color" + str(i) + "]", str(colors['color'+str(i)]))

    filedata = filedata.replace("[background]", str(colors['color0']))
    filedata = filedata.replace("[background_light]", str(colors['color8']))
    filedata = filedata.replace("[foreground]", str(colors['color15']))
    filedata = filedata.replace("[foreground_dark]", str(colors['color7']))

    return filedata

def linkWallpaperToFolder(wallpaper, file_path):
    image_symlink = os.path.join(file_path, 'image')
    if os.path.isfile(image_symlink):
        os.remove(image_symlink)
    os.symlink(wallpaper, image_symlink)