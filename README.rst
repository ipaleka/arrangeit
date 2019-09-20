.. image:: https://github.com/ipaleka/arrangeit/raw/master/arrangeit/resources/logo.png
   :width: 400px
   :alt: arrangeit logo with slogan
   :align: left

.. image:: https://travis-ci.org/ipaleka/arrangeit.svg?branch=master
    :target: https://travis-ci.org/ipaleka/arrangeit
.. image:: https://coveralls.io/repos/github/ipaleka/arrangeit/badge.svg?branch=master
    :target: https://coveralls.io/github/ipaleka/arrangeit?branch=master



**arrangeit** is a cross-platform desktop utility that helps you placing your
desktop's open windows. It is a utility mostly based on the mouse movements, with
some keyboard shortcuts as helpers.


Installation
============

Binary distribution
-------------------

You may find **arrangeit v0.3alpha** installation packages for Debian/Ubuntu and
MS Windows in the releases_ page.

.. _releases: https://github.com/ipaleka/arrangeit/releases


Debian/Ubuntu
^^^^^^^^^^^^^

Run the following commands after you downloaded and extracted the archive in a
temporary directory:

.. code-block:: bash

  $ sudo apt-get install python3-pil.imagetk python3-xlib
  $ cd tmp_directory
  $ sudo dpkg -i python3-pynput_1.4.2_all.deb
  $ sudo dpkg -i arrangeit_0.3alpha_all.deb


Run the executable with:

.. code-block:: bash

  $ arrangeit


MS Windows
^^^^^^^^^^

Extract the archive in a directory of your choice and run the ``arrangeit.exe``
executable inside it.


Source distribution
-------------------

You'll find a detailed explanation in the installation_ and development_ pages.

Use the following commands in Ubuntu for a quick start:

.. code-block:: bash

  $ sudo apt-get install python3-dev git gcc libgirepository1.0-dev \
      libcairo2-dev pkg-config gir1.2-gtk-3.0 gir1.2-wnck-3.0

  $ cd ~/projects
  $ git clone https://github.com/ipaleka/arrangeit.git
  $ mkdir venvs
  $ python3 -m venv venvs/arrangeit
  $ source venvs/arrangeit

  (arrangeit) $ cd arrangeit
  (arrangeit) $ python -m pip install -r requirements/linux.txt

  (arrangeit) $ python -m arrangeit


Basic usage
===========

Move your mouse to set the future position of the window. You may change the active
corner either manually, by pressing the **Ctrl** key on your keyboard, or dynamically
through the snapping functionality (when a moving window snaps to some window with a
side not connected to the currently active corner).

By pressing the left mouse button (or by pressing the **Enter** key on your keyboard)
you set the future position of the window and moving the mouse afterward resizes the
main window. Press the left mouse button again to confirm the future size.

To move the current window on another workspace you should press the wanted workspace
number on your keyboard. As an alternative, you may first release the mouse by
clicking the middle mouse button or by pressing the **Shift** key on keyboard, and
then click the wanted workspace box with your mouse.

Click a window title in the listed windows area to start operating from some other
window.

Click |minimize| (or |restore|) icon inside the title box to change the minimized
state of the current window.

Click |fixed| (or |resizable|) icon if you want to change just the position of the
current window, without changing its size (and vice versa).

**arrangeit v0.3alpha** stops running either when all the windows are exhausted or
when you press the **Esc** key on your keyboard.

screencast_

.. |resizable| image:: ./docs/_static/resize.png
.. |fixed| image:: ./docs/_static/move.png
.. |restore| image:: ./docs/_static/restore.png
.. |minimize| image:: ./docs/_static/minimize.png


Keyboard shortcuts
==================

======  ===================  =============
 Key    Mouse                Action
        counterpart
======  ===================  =============
Enter   left-click           confirm position
Esc     Quit button          quit program
Space   right-click          skip window
Ctrl    *by snapping*        cycle corner
Shift   middle-click         release mouse
R       resizable icon       turn on/off resizing phase
M       minimize icon        make window minimized/restored
1-9     click workspace      change workspace
F1-F12  click listed window  restart from selected window
======  ===================  =============

Support
=======

Please `create an issue`_ for any problem you've encountered regarding arrangeit
installation, usage or development.

Don't hesitate to send `a direct message or a tweet`_ if you have any questions or
concerns. Or just `send an email`_.


Contributing
============

Any help is appreciated and your pull requests are welcome, Please help in reaching
arrangeit's three major milestones `in the roadmap`_: 0.4beta version with Mac OS X
support, 0.5 as the first stable version and the 1.0 version.

Meanwhile, please make the initial step by clicking the Star button from above!


License
=======

This project is licensed under the GNU General Public License v3.0 - see the
legal_ page for details.

.. _installation: https://arrangeit.readthedocs.io/en/latest/installation.html
.. _development: https://arrangeit.readthedocs.io/en/latest/development.html
.. _legal: https://arrangeit.readthedocs.io/en/latest/legal.html
.. _screencast: https://vimeo.com/351440620
.. _create an issue: https://github.com/ipaleka/arrangeit/issues
.. _a direct message or a tweet: https://twitter.com/arrangeit1
.. _send an email: arrangeit@protonmail.com
.. _in the roadmap: https://github.com/ipaleka/arrangeit/wiki/Roadmap
