# KADAI
Simple wallpaper and lockscreen manager for tiling window managers.

This project is heavily inspired by [pywal](https://github.com/dylanaraps/pywal) with the main color generator being based off of it.
KADAI is a project aimed at making theme alignment easier for the entire desktop experience, and is aimed towards users of tiling window managers (mainly i3wm).
KADAI generates an Xresources file, sets the background and optionally creates a lockscreen background for i3lock.
The main philosophy behind KADAI is to not edit any predefined configuration files, but instead works as an extra layer to your customised layout.

## How to use
If you ever get stuck on the syntax of this command, execute: `kadai -h` or `kadai [subcommand] -h` for the list of avaliable arguments.
This script is split into two sections, the theme and the lockscreen sections

### theme
This command is executed using `kadai theme ...` and is used to manage the wallpaper and theme.

The arguments are the following:

| Argument  | Usage |
|-----------|-----------------------------------------------------|
| -h, --help| Shows the help message for the theme subcommand |
| -g        | Switch for generating themes |
| -i        | The input file |
| -l        | Apply the same image as the lockscreen |
| -p        | Use the last set theme |

### lockscreen
This command is executed using `kadai lockscreen ...` and is used to manage the i3lock wallpaper.

The arguments are the following:

| Argument  | Usage |
|-----------|-----------------------------------------------------|
| -h, --help| Shows the help message for the wallpaper subcommand |
| -g        | Switch for generating the lockscreen |
| -i        | The input file |

### cache
This command is executed using `kadai clear ...` and is used to clear the cache for the app

The arguments are the following:

| Argument | Usage |
|----------|-------|
| --all    | Clears all the cache |
| --type   | Clears depending on type. Options are theme and lockscreen |

## Installation

### Dependencies

#### Python
 - [tqdm](https://pypi.org/project/tqdm/)
 - [Pillow](https://pypi.org/project/Pillow/)
 - [colorthief](https://pypi.org/project/colorthief/)

#### Additional Programs
 - [xrandr](https://www.archlinux.org/packages/extra/x86_64/xorg-xrandr/)
 - [feh](https://www.archlinux.org/packages/extra/x86_64/feh/)
 - [ImageMagick](https://www.archlinux.org/packages/extra/x86_64/imagemagick/)

### Process
To install this, please check under the releases and place the executable under a path directory (for example `$HOME/.bin/`)

#### Creating from code
Under the directory where this file is located, run the `create_binary.sh` to create the binary. Place this binary under a path directory.

## Postscripts
Post scripts are executables that are run after one of the sub commands are completed.
To create a postscript, do the following:
1. Create a file with the following naming convention: `##-type-name`.

	 - Where `##` is a number from 00-99 (The files are loaded in numerical order)
	 - Where `type` is the type (theme, lockscreen)
 	 - Where `name` is the name of it

2. Add this file under ~/.local/share/kadai/postscripts
3. Make it executable (under linux `chmod +x filename` works)

For examples of postscripts look under `examples/postscripts`

## Templates
The template files are files used during the creation of theme files.
Place or create these template files under `~/.local/share/kadai/templates/`.

These files **must** follow the Xresources rules and is an overlay of using the Xresources file
This feature is only intead to be used for colors, as that is all that will be replaced.

For examples of template files look under `examples/templates`
