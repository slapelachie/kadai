
# KADAI
Simple wallpaper manager for tiling window managers.

![Run Tests](https://github.com/slapelachie/kadai/workflows/Run%20Tests/badge.svg)

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/L3L726D8I)

This project is heavily inspired by [pywal](https://github.com/dylanaraps/pywal) with the main color generator being based off of it.
KADAI is a project aimed at making theme alignment easier for the entire desktop experience, and is aimed towards users of tiling window managers (mainly i3wm).
The main philosophy behind KADAI is to not edit any predefined configuration files, but instead works as an extra layer to your customised layout.

## Usage
To get the usage for the command, use `$ kadai --help`.
You can also the find the usage directly below.
```
usage: kadai [-h] [-v] [-q] [-g] [-i "path/to/dir"] 
			 [-p] [--override][--clear]

Generate and switch wallpaper themes

optional arguments:
  -h, --help        show this help message and exit
  -q                Allow only error logging
  -g                generate themes
  -i "path/to/dir"  the input file
  -p                Use last set theme
  --override        Override exisiting themes
  --clear           Clear all data relating to KADAI
  --backend         Switches to a different backend (hue/vibrance/k_means)
  --progress        Shows the progress of the command
  --warrenty        Shows the programs warrenty
  --light           Switch to using a light theme varient
```

### Important Note
kadai does not work out of the box, as it relies on templates and hooks to be functional.
This is covered in depth [here](https://github.com/slapelachie/kadai/wiki/ExtraFiles).

### Basic commands
#### The Update Command
This is the command that you would most likely be using the most.
This command should be used to update the theme.
The command is as follows.
```
$ kadai -i /path/to/file/or/directory
```
There are two ways this command can be used. The first instance is to directly apply the theme to a specified wallpaper.
This would look like
```
$ kadai -i ~/Wallpapers/a-cool-wallpaper.png
```
The other way this command could be applied is to have it pick a random wallpaper from a directory.
This would look like
```
$ kadai -i ~/Wallpapers/
```

#### The Generate Command
The **update** command generates the colorschemes automatically for the wallpaper parsed.
However, if you wanted to save an extra few seconds every time the wallpaper is updated, it might be necessary to pre-generate the themes beforehand. The command to do this is as follows
```
$ kadai -gi /path/to/file/or/directory
```
The most often use-case scenario would be to pre-generate a folder of Wallpapers that will be randomly picked by the update command. This would look like
```
$ kadai -gi ~/Wallpapers/
```

#### The Preserve Command
If you are a user that likes to have a consistant wallpaper, then having the same wallpaper load up is a must. Using the preserve command allows for you to load up the last used wallpaper. The command is as follows
```
$ kadai -p
```
If you've never loaded a wallpaper with kadai before, this command will fail as it relies on applying the last used wallpaper.

### Backends
There are multiple different backends currently supported which change the way the colors are generated.
| Engine   | Description                                                                                                                                                                                                                   |
|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| hue      | For hue based generation. The generator picks the most dominant color  and generates the other colors based off of that to compliment it. This stops the unknown color problem where you don't know which color is which in X |
| vibrance | Generates colors by choosing the top 16 most dominant colors and sorting them into the top 7 most vibrant colors                                                                                                              |
| k_means  | An experimental backend that uses k-means to find the most dominant colors, the output is very similar to vibrance backend                                                                                                    |


## Installation

### Dependencies
- Linux
- A X11 compatible terminal emulator
- Python 3+

#### Notes
All tests have been performed on Ubuntu and Arch, so there is no guarentee that it will work on any other distribution.

### Installation

#### From PyPI (The Python Package Index)
This gets updated with every release I push, which is usually when I find the script to be stable enough to work without issues.

For a system wide install (requires superuser permissions), issue the command 
```
# pip install kadai
```

For a user only install, issue the command 
```
$ pip install --user kadai
```

This method requires `$HOME/.local/bin/` to be registered in the `PATH` environmental variable.
This can be achieved by adding `export PATH=$PATH:$HOME/.local/bin/` into your `.bashrc` or `.profile`.

#### From source (github repo)
Installing from source is not recommended, as it may contain bugs or problems that I haven't fixed.
If you still want to go ahead issue the following commands

```
$ git clone https://github.com/slapelachie/kadai.git
$ cd kadai
```

If you want to install it system wide (requires superuser permissions), run
```
# pip install .
```
If you want to install it for the user, run
```
$ pip install --user .
```

### Running Tests
If you find the need to run tests, execute the following commands
```
$ git clone https://github.com/slapelachie/kadai.git
$ cd kadai
$ python setup.py develop
$ pip install --user pytest
$ pytest
```

## TODO
* Allow printing colors to stout

## Links
\[[Required Files](https://github.com/slapelachie/kadai/wiki/ExtraFiles)\]
\[[Required Files - Applications](https://github.com/slapelachie/kadai/wiki/ExtraFiles-Aplications)\]
