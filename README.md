# KADAI
Simple wallpaper manager for tiling window managers.

This project is heavily inspired by [pywal](https://github.com/dylanaraps/pywal) with the main color generator being based off of it.
KADAI is a project aimed at making theme alignment easier for the entire desktop experience, and is aimed towards users of tiling window managers (mainly i3wm).
The main philosophy behind KADAI is to not edit any predefined configuration files, but instead works as an extra layer to your customised layout.

## How to use
If you ever get stuck on the syntax of this command, execute: `kadai -h` for the list of avaliable arguments.

### Arguments
The arguments are the following:

| Argument    | Usage |
|-------------|-----------------------------------------------------|
| -h, --help  | Shows the help message for the theme subcommand |
| -g          | Switch for generating themes |
| -i          | The input file |
| -l          | Apply the same image as the lockscreen |
| -p          | Use the last set theme |
| -v          | Allows verbose logging |
| -q          | Only show errors |
| --clear     | Clear the cache |
| --overwrite | Overwrite previously existing files |

## Installation

### Dependencies

#### Python
 - [tqdm](https://pypi.org/project/tqdm/)
 - [Pillow](https://pypi.org/project/Pillow/)
 - [colorthief](https://pypi.org/project/colorthief/)

### Installation

#### System Wide Install
To install system wide, run `$ pip install kadai` or if from source `$ pip install .`

#### User Install
To install for just the user, run `$ pip install --user kadai` or if from source `$ pip install --user .`

This method assumes that the `~/.local/bin/` is included in the `$PATH` variable.

## Postscripts
Post scripts are executables that are run after one of the sub commands are completed.
The scripts take in an argument which contains the path to the image, this can be accessed through `${1}` in the script.

To create a postscript, do the following:
1. Create a file with the following naming convention: `##-name`.

	 - Where `##` is a number from 00-99 (The files are loaded in numerical order)
 	 - Where `name` is the name of it

2. Add this file under ~/.local/share/kadai/postscripts
3. Make it executable (e.g. `chmod +x filename`)

For examples of postscripts look under `examples/postscripts`

## Templates
The template files are files used during the creation of theme files.
Place or create these template files under `~/.local/share/kadai/templates/`.

These files **must** follow the Xresources rules and is an overlay of using the Xresources file
This feature is only intead to be used for colors, as that is all that will be replaced.

For examples of template files look under `examples/templates`
