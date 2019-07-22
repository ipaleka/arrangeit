Installation
============

You may download **arrangeit v0.3alpha** either in the form of a binary distribution
package (pick your platform and preferred Python version from the project's releases
page on Github) or as a source package distribution.

Minimum requirements for Python is version 3.5.


GNU/Linux
---------

Binary distribution
^^^^^^^^^^^^^^^^^^^

For now, only Debian/Ubuntu binary releases for Python 3.5, 3.6 and 3.7 can be
downloaded from the releases_ page.

Download binaries of your choice and place them in a temporary directory. Install
**arrangeit** by typing the following commands in terminal:

.. code-block:: bash

  $ sudo apt-get install python3-pil.imagetk python3-xlib
  $ cd tmp_directory
  $ sudo dpkg -i python3-pynput_1.4.2_all.deb
  $ sudo dpkg -i arrangeit_0.3alpha_all.deb


Run the executable with:

.. code-block:: bash

  $ arrangeit


Uninstallation
""""""""""""""

If you want you may uninstall the software with:

.. code-block:: bash

  $ sudo apt-get purge arrangeit
  $ sudo apt-get autoremove --purge


Also, if you've saved some data or changed some settings from the Options dialog,
then you may delete every trace of that by removing the data directory:

.. code-block:: bash

  $ rm -rf ~/.local/share/arrangeit


Source distribution
^^^^^^^^^^^^^^^^^^^

Use the following commands in Ubuntu to prepare and run **arrangeit**:

.. code-block:: bash

  # install requirements
  $ sudo apt-get install python3-dev git gcc \
      libgirepository1.0-dev libcairo2-dev pkg-config gir1.2-gtk-3.0

  # change current directory to the one where you keep your projects
  $ cd ~/projects

  # clone arrangeit repository (or you may download it as a compressed directory)
  $ git clone https://github.com/ipaleka/arrangeit.git

  # create directory for the virtual environments if you don't have it already
  $ mkdir venvs
  # create virtual environment for arrangeit
  $ python3 -m venv venvs/arrangeit
  # activate newly created virtual environment
  $ source venvs/arrangeit

  # install Python dependencies
  (arrangeit) $ cd arrangeit
  (arrangeit) $ python -m pip install -r requirements/linux.txt

  # run arrangeit
  (arrangeit) $ python -m arrangeit


MS Windows
----------

Binary distribution
^^^^^^^^^^^^^^^^^^^

Provided binary release downloaded from the releases_ page is in the form of a
compressed directory.

Extract it in a directory of your choice and run the ``arrangeit.exe`` executable
by clicking it. You may also, of course, create a shortcut to that executable and
place it on the desktop or in some other place of choice.

.. _releases: https://github.com/ipaleka/arrangeit/releases


Uninstallation
""""""""""""""

No runtime files will be placed outside that directory during a run. If you've
changed some settings or saved the data in the Options dialog, then your
configuration files would be saved in ``arrangeit`` directory under your user's
directory.

If you want to delete every trace of **arrangeit** software, then you should delete
that directory (typically ``c:\Users\yourusername\arrangeit``) and the directory
where you extracted the binary distribution.


Source distribution
^^^^^^^^^^^^^^^^^^^

You should install `Python 3`_ first in order to run **arrangeit** from the source in
MS Windows.

Then you should either download `source archive`_ and extract it in a directory of
your choice or you may clone **arrangeit** repository (detailed instructions are in
the development_ page).

.. _Python 3: https://www.python.org/downloads/
.. _source archive: https://github.com/ipaleka/arrangeit/archive/master.zip
.. _development: https://github.com/ipaleka/arrangeit/blob/master/docs/development.rst

You should take the following steps in order to prepare and run **arrangeit** from
source distribution in MS Windows:

.. code-block:: batch

  :: change current directory to the one where you keep your projects
  cd projects

  :: create directory for the virtual environments if you don't have it already
  mkdir venvs
  :: create virtual environment for arrangeit
  python -m venv venvs\arrangeit
  :: activate newly created virtual environment with
  venvs\arrangeit\Scripts\activate.bat

  :: enter the extracted source distribution directory
  (arrangeit) cd arrangeit

  :: install Python dependencies
  (arrangeit) python -m pip install -r requirements/windows.txt

  :: run arrangeit
  (arrangeit) python -m arrangeit
