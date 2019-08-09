---
layout: post
title:  "arrangeit v0.3alpha has been released!"
date:   2019-07-30 20:37:09 +0200
---
TL; DR end users, Pythonistas, graphic designers and proofreaders are invited to join a brand new open-source multi-platform Python project

[arrangeit v0.3alpha in action](https://vimeo.com/351440620)

## About

**arrangeit** - cross-platform desktop utility for easy windows management

Version [0.91](https://github.com/ipaleka/arrangeit/tree/master/assets) was the last published version of a Win95/98 desktop utility named ArrangeIt.

Twenty years later, new software with the name **arrangeit** is born. It has been developed from the scratch in Python and the [initial public release v0.3alpha](https://github.com/ipaleka/arrangeit/releases/tag/v0.3alpha) is now available to download from the Github. Please bear in mind that this version is alpha software and it's not suitable for production.

## Installation

### Binary distribution

Version 0.3alpha is available as the binary distribution for Debian/Ubuntu and MS Windows (32 and 64-bit versions).

In Ubuntu, you should have at least Python version 3.5 installed. Extract the archive in temporary directory and run the following commands:

    $ sudo apt-get install python3-pil.imagetk python3-xlib
    $ cd tmp_directory
    $ sudo dpkg -i python3-pynput_1.4.2_all.deb
    $ sudo dpkg -i arrangeit_0.3alpha_all.deb

    # run the program with
    $ arrangeit

In Windows, just extract the archive and run the `arrangeit.exe` executable inside it.

### Source distribution

You should have Python 3 installed to run **arrangeit** from the source. For the other dependencies, you may find instructions for various platforms [in the documentation](https://arrangeit.readthedocs.io/en/latest/development.html). To prepare a start on Ubuntu you may run the following command:

    $ sudo apt-get install python3-dev git gcc libgirepository1.0-dev libcairo2-dev pkg-config gir1.2-gtk-3.0 gir1.2-wnck-3.0

Download source archive as a compressed file or clone the git repository with:

    $ cd ~/projects
    $ git clone https://github.com/ipaleka/arrangeit.git

You should create and activate a separate virtual environment for arrangeit:

    $ mkdir venvs
    $ python3 -m venv venvs/arrangeit
    $ source venvs/arrangeit

And from the activated virtual environment run the following commands to install Python dependencies:

    (arrangeit) $ cd arrangeit
    (arrangeit) $ python -m pip install -r requirements/linux.txt  # or windows.txt or darwin.txt

Run arrangeit with:

    (arrangeit) $ python -m arrangeit


## Basic usage

Move your mouse to set the future position of the window. You may change the active
corner either manually, by pressing the **Ctrl** key on your keyboard, or dynamically
through the snapping functionality (when a moving window snaps to some window with a
side not connected to the currently active corner).

By pressing the left mouse button (or by pressing the **Enter** key on your keyboard)
you set the future position of the window and moving the mouse afterward resizes the
main window. Press the left mouse button again to confirm the future size.

To move the current window on another workspace you should press the wanted workspace
number on your keyboard. As an alternative, you may first release the mouse by
clicking the middle mouse button or by pressing the **Shift** key on the keyboard, and
then click the wanted workspace box with your mouse.

Click a window title in the listed windows area to start operating from some other
window.

Click the minimize/restore icon inside the title box to change the minimized state of the current window.

Click the fixed/resizable icon if you want to change just the position of the current window, without changing its size (and vice versa).

## Known issues

The list of issues can be found on [Github pages](https://github.com/ipaleka/arrangeit/issues). Please feel free to add a new issue for any purpose connected with the arrangeit development beside praising and condemning - for such purposes please use this thread. xD

- **arrangeit** in GNU/Linux works under X Window System only - Wayland is not supported yet and you're all welcome to propose possible guidelines in the [related issue](https://github.com/ipaleka/arrangeit/issues/5)
- Mac OS X functionality is planned for the next release **0.4beta**
- X-mouse under Windows 10 is sometimes preventing the binary distribution executable to start
- no workspaces/virtual desktops functionality for the older versions of Windows. Windows 10 is the first version having an official API for virtual desktops -  if some custom implementation has been quite popular for the previous Windows versions then please let me know about it
- current graphic design is kind of MVPish; all suggestions are welcome






[v0.3alpha]: https://github.com/ipaleka/arrangeit/releases/tag/v0.3alpha
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
