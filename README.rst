.. image:: https://github.com/ipaleka/arrangeit/raw/master/arrangeit/resources/logo.png
   :width: 400px
   :alt: arrangeit logo with slogan
   :align: left

About
=====

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
executable.


Source distribution
-------------------

You'll find a detailed explanation in the installation_ and development_ pages.

Use the following commands in Ubuntu for a quick start:

.. code-block:: bash

  $ sudo apt-get install python3-dev git gcc libgirepository1.0-dev libcairo2-dev pkg-config gir1.2-gtk-3.0

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



Licence
=======

This project is licensed under the GNU General Public License v3.0 - see the
legal_ page for details.

.. _installation: https://github.com/ipaleka/arrangeit/blob/master/docs/installation.rst
.. _development: https://github.com/ipaleka/arrangeit/blob/master/docs/development.rst
.. _legal: https://github.com/ipaleka/arrangeit/blob/master/docs/legal.rst
