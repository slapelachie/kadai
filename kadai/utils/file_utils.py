"""File based utilities"""
import hashlib
import os
import re
import subprocess
from typing import List
from PIL import Image, UnidentifiedImageError


class NoPreGenThemeError(Exception):
    """Error raised when there is no pre generated theme"""


def get_data_path() -> str:
    """
    Returns the users data path

    Returns:
        (str): the users data path
    """
    if "XDG_DATA_HOME" in os.environ:
        return os.path.join(os.getenv("XDG_DATA_HOME"), "kadai")

    return os.path.expanduser("~/.local/share/kadai")


def get_cache_path() -> str:
    """
    Returns the users cache path

    Returns:
        (str): the users cache path
    """
    if "XDG_CACHE_HOME" in os.environ:
        return os.path.join(os.getenv("XDG_CACHE_HOME"), "kadai")

    return os.path.expanduser("~/.cache/kadai")


def get_config_path() -> str:
    """
    Returns the users config path

    Returns:
        (str): the users config path
    """
    if "XDG_CONFIG_HOME" in os.environ:
        return os.path.join(os.getenv("XDG_CONFIG_HOME"), "kadai")

    return os.path.expanduser("~/.config/kadai")


def md5(string: str) -> str:
    """
    Generates a md5 hash based on the parsed string

    Arguments:
        string (str): a string to be encoded

    Returns:
        (str): the md5 output of the inputted string
    """

    hash_md5 = hashlib.md5(str(string).encode())
    return hash_md5.hexdigest()


def md5_file(file_path: str) -> str:
    """
    Generates a md5 hash based on the file parsed

    Arguments:
        file_name (str): location of the file ('/home/bob/pic.png')

    Returns:
        (str): md5 output of the file
    """

    hash_md5 = hashlib.md5()

    with open(file_path, "rb") as fin:
        for chunk in iter(lambda: fin.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


def check_if_image(image_file_path: str) -> bool:
    """
    Verifies if the given image file is an image

    Arguments:
        image_file_path (str): the path to the image file

    Returns:
        (bool): if the file is valid, returns true, otherwise false
    """
    try:
        Image.open(image_file_path).verify()
        return True
    except (ImportError, UnidentifiedImageError):
        return False


def get_directory_images(image_directory: str) -> List[str]:
    """
    Get a list of all images in a directory

    Arguments:
        image_directory (str): the directory where the images are stored

    Returns:
        (List[str]): a list containing the absolute paths to the images
    """
    file_types = ("png", "jpg", "jpeg")
    return [
        os.path.abspath(os.path.join(image_directory, image.name))
        for image in os.scandir(image_directory)
        if image.name.lower().endswith(file_types)
        and check_if_image(os.path.join(image_directory, image.name))
    ]


def get_image_list(image_path: str) -> List[str]:
    """
    Get a list of images from the image path, if the path is to an image file
    will only return a list with that one image. Otherwise returns a list of all
    images in the directory parsed

    Arguments:
        image_path (str): path to image or image directory

    Returns:
        (List[str]): the list of images absolute paths
    """
    image_path = os.path.expanduser(image_path)
    if os.path.isfile(image_path):
        if check_if_image(image_path):
            return [os.path.abspath(image_path)]

        raise ValueError("Specified file is not an image!")

    if os.path.isdir(image_path):
        images = get_directory_images(image_path)
        if len(images) == 0:
            raise FileNotFoundError("Specified directory does not contain any images!")

        return images

    raise ValueError("Unknown file type!")


def get_hooks(**kwargs) -> List[str]:
    """
    Returns a list of hooks in a given directory

    Arguments:
        **hooks_directory (str): the path to the hooks directory

    Returns:
        (List[str]): A list containing the paths to the scripts
    """
    hooks_directory = kwargs.get(
        "hooks_directory", os.path.join(get_config_path(), "hooks")
    )
    os.makedirs(hooks_directory, exist_ok=True)

    scripts = [
        f
        for f in os.listdir(hooks_directory)
        if re.match(r"^([0-9]{2}-\w+)", f)
        and os.access(os.path.join(hooks_directory, f), os.X_OK)
    ]
    scripts.sort()
    return scripts


def run_hooks(**kwargs):
    """
    Runs the hooks within a given directory

    Arguments:
        **use_light_theme (bool): whether to enable light theme options
        **hooks_directory (str): the path to the hooks directory
    """
    use_light_theme = kwargs.get("use_light_theme", False)
    hooks_directory = kwargs.get(
        "hooks_directory", os.path.join(get_config_path(), "hooks")
    )
    scripts = get_hooks(hooks_directory=hooks_directory)

    for script in scripts:
        script = os.path.join(hooks_directory, script)

        with open(os.devnull, "w", encoding="UTF-8") as devnull:
            subprocess.run(
                [script, str(use_light_theme).lower()],
                stdout=devnull,
                stderr=subprocess.STDOUT,
                check=True,
            )
