Development
===========

This section is about the requirements necessary to use this project in development.

Platforms
---------

GNU/Linux
^^^^^^^^^

Ubuntu
""""""

.. code-block:: bash

  sudo apt-get install libgirepository1.0-dev gcc \
    libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0


To build latexpdf documentation:

.. code-block:: bash

  sudo apt-get install texlive texlive-latex-extra latexmk


elementaryOS 5.0 (juno)
"""""""""""""""""""""""

.. code-block:: bash

  apt-get install python3-venv gitk git-gui pkg-config \
    python3-tk python3-dev libgirepository1.0-dev


Debian stable (Stretch)
"""""""""""""""""""""""

.. code-block:: bash

  apt-get install python3-dev python3-venv gitk git-gui python3-tk \
    libcairo2-dev libgirepository1.0-dev gir1.2-gtk-3.0 gir1.2-wnck-3.0


Manjaro 18.04 Xfce
""""""""""""""""""

.. code-block:: bash

  sudo pacman -S gobject-introspection tk


MS Windows
^^^^^^^^^^


Darwin
^^^^^^

Download official installer from https://www.python.org/downloads/, download and install Python by executing .pkg file 
and finally run post-install script `Install Certificates.command`.


Tools
-----


fpm
^^^

dependency: `virtualenv-tools3` (`pip3 install virtualenv-tools3`)

fpm_ is used to build GNU/Linux installation package.

.. _fpm: https://github.com/jordansissel/fpm

Run the following command inside project's root directory to create Debian installation package:

.. code-block:: bash

fpm -s python -t deb -n arrangeit --category=misc --license=GPLv3 -d "python3-pil" -d "python3-pip" -d "python3-gi" -d "python3-gi-cairo" -d "gir1.2-gtk-3.0" -d "python3-xlib" -m "Ivica Paleka <ipaleka@hopemeet.me>" --no-python-dependencies --python-obey-requirements-txt --python-bin=python3 --python-pip=pip3 --force --log=debug setup.py
fpm -s virtualenv -t deb -n arrangeit --category=misc --license=GPLv3 -d "python3-pip" -d "python3-gi" -d "python3-gi-cairo" -d "gir1.2-gtk-3.0" -m "Ivica Paleka <ipaleka@hopemeet.me>" -a all -v 0.3alpha --description="Cross-platform desktop utility for easy windows management" --url=https://github.com/ipaleka/arrangeit --python-bin=python3 --python-pip=pip3 --virtualenv-setup-install --force --log=debug requirements.txt

  fpm -s python -t deb -n arrangeit --category=misc  \
    -d "python3-pil" -d "python3-pip" -d "python3-xlib" \
    -d "python3-gi" -d "python3-gi-cairo" -d "gir1.2-gtk-3.0" \
    -m "Ivica Paleka <ipaleka@hopemeet.me>" \
    --no-python-dependencies --python-obey-requirements-txt \
    --force --log=debug setup.py

TODO: add script to parameter `--deb-after-purge` which will delete local/share/arrangeit directory


PyInstaller
^^^^^^^^^^^

PyInstaller_ is used to build MS Windows installation package.

.. _PyInstaller: https://www.pyinstaller.org/

`starter.py` script is created in the project's root directory for the purpose of PyInstaller's dependencies collecting.
There's specification file `arrangeit_pyinstaller.spec` in the same directory used to produce MS Windows executable by the following call:

.. code-block:: bash

  python -OO -m PyInstaller `arrangeit_pyinstaller.spec


stdeb
^^^^^

.. code-block:: bash

  sudo apt-get install python3-all
  pip3 install stdeb --user
  python setup.py sdist
  cd dist
  py2dsc-deb arrangeit-0.2.4.tar.gz


py2deb
^^^^^^

.. code-block:: bash

  sudo apt-get install dpkg-dev fakeroot


dh-virtualenv
^^^^^^^^^^^^^

.. code-block:: bash

  sudo apt-get install build-essential debhelper devscripts equivs


black
^^^^^

Code should be formatted by `black` before commit.

Install `black` with:

.. code-block:: bash

  python3 -m pip install black

Run it from the root directory by:

.. code-block:: bash

  black arrangeit


pyflakes
^^^^^^^^

Install `pyflakes` linter with:

.. code-block:: bash

  python3 -m pip install pyflakes

Run it from the root directory by:

.. code-block:: bash

  python3 -m pyflakes arrangeit


SonarQube
^^^^^^^^^

https://docs.sonarqube.org/latest/setup/get-started-2-minutes/


Starting server
^^^^^^^^^^^^^^^

.. code-block:: bash

  ~/opt/repos/sonarqube-7.7/bin/linux-x86-64/sonar.sh console


Starting scanner
^^^^^^^^^^^^^^^^

https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner

.. code-block:: bash
  :caption: ~/.bashrc

  export PATH=$PATH:~/opt/repos/sonar-scanner/bin


Just run in the root directory of the project:

.. code-block:: bash

  sonar-scanner


Administration
^^^^^^^^^^^^^^

Prepare coverage.xml by running in the project's root directory:

.. code-block:: bash

  python -m pytest -v --cov-report xml:tests/coverage-linux.xml --cov=arrangeit


http://localhost:9000

Login as `admin/admin`.