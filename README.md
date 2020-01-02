# KADAI
Simple wallpaper and lockscreen manager for tiling window managers.

This project is heavily inspired by [pywal](https://github.com/dylanaraps/pywal) with the main color generator being based off of it.
KADAI is a project aimed at making theme alignment easier for the entire desktop experience, and is aimed towards users of tiling window managers (mainly i3wm).
KADAI generates an Xresources file, sets the background and optionally creates a lockscreen background for i3lock.
The main philosophy behind KADAI is to not edit any predefined configuration files, but instead works as an extra layer to your customised layout.

## How to use
If you ever get stuck on the syntax of this command, execute: `kadai -h` or `kadai [subcommand] -h` for the list of avaliable arguments.

This script is split into two sections, the wallpaper and the lockscreen sections

### wallpaper
This command is executed using `kadai wallpaper ...` and is used to manage the wallpaper and theme.

The arguments are the following:

| Argument  | Usage |
|-----------|-----------------------------------------------------|
| -h, --help| Shows the help message for the wallpaper subcommand |
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

## Installation

### Prerequisites
Will get to this one day

### Process
Place template files under `~/.config/kadai/templates/`

Under the directory where this file is located, run the `create_binary.sh` to create the binary. Place this binary under a path directory.
