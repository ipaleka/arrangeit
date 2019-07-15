Installation
============

You may download **arrangeit v0.3alpha** either in the form of a binary distribution package (pick your platform and preferred Python version from the project's releases_ page on Github) or as a source package distribution.

Minimum requirements for Python is version 3.5.


GNU/Linux
---------

Binary distribution
^^^^^^^^^^^^^^^^^^^

For now, only Debian/Ubuntu binary releases for Python 3.5, 3.6 and 3.7 can be downloaded from the releases_ page.

Download binaries of your choice and place them in a temporary directory. Install the software by typing the following commands in terminal:

.. code-block:: bash

  sudo apt-get install python3-pil.imagetk python3-xlib
  cd tmp_directory
  sudo dpkg -i python3-pynput_1.4.2_all.deb
  sudo dpkg -i arrangeit_0.3alpha_all.deb


Run the executable with:

.. code-block:: bash

  arrangeit


Uninstallation
""""""""""""""

If you want you may uninstall the software with:

.. code-block:: bash

  sudo apt-get purge arrangeit
  sudo apt-get autoremove --purge


Also, if you've saved some data or changed some settings from the Options dialog, then you may delete every trace of that by removing the data directory:

.. code-block:: bash

  rm -rf ~/.local/share/arrangeit


Source distribution
^^^^^^^^^^^^^^^^^^^



MS Windows
----------

Binary distribution
^^^^^^^^^^^^^^^^^^^

Provided binary release downloaded from the releases_ page is in the form of a compressed directory.

Extract it in a directory of your choice and run the `arrangeit.exe` executable by clicking it. You may also, of course, create a shortcut to that executable and place it on the desktop or in some other place of choice.


Uninstallation
""""""""""""""

No runtime files will be placed outside that directory during a run. If you've changed some settings or saved the data in the Options dialog, then your configuration files would be saved in `arrangeit` directory under your user directory.

If you want to delete every trace of **arrangeit** software, then you should delete that directory (typically ``c:\Users\yourusername\arrangeit``) and the directory where you extracted the binary distribution.

Source distribution
^^^^^^^^^^^^^^^^^^^

.. _releases: https://github.com/ipaleka/arrangeit/releases
