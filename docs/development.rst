Development
===========

This section is about the requirements necessary to develop **arrangeit** software.

System requirements
-------------------

GNU/Linux
^^^^^^^^^

Ubuntu
""""""

To start **arrangeit** development on Ubuntu, you should install some system packages
by issuing the following command:

.. code-block:: bash

  $ sudo apt-get install python3-dev git gcc pkg-config libcairo2-dev \
      libgirepository1.0-dev gir1.2-gtk-3.0  gir1.2-wnck-3.0


If you are planning to build latexpdf documentation then you should install some
additional packages with:

.. code-block:: bash

  $ sudo apt-get install texlive texlive-latex-extra latexmk


elementaryOS 5.0 (juno)
"""""""""""""""""""""""

.. code-block:: bash

  $ sudo apt-get install python3-dev python3-venv git python3-tk \
      pkg-config libgirepository1.0-dev


Debian Stretch
""""""""""""""

.. code-block:: bash

  $ su
  # apt-get install python3-dev python3-venv python3-tk git pkg-config \
      libcairo2-dev libgirepository1.0-dev gir1.2-gtk-3.0 gir1.2-wnck-3.0


Debian Buster
"""""""""""""

.. code-block:: bash

  $ su
  # apt-get install python3-dev python3-venv python3-tk git gcc \
      pkg-config libcairo2-dev libgirepository1.0-dev


Manjaro 18.04 Xfce
""""""""""""""""""

.. code-block:: bash

  $ sudo pacman -S gobject-introspection tk


MS Windows
^^^^^^^^^^

Official `Python 3 installer`_ and `git for Windows`_ probably represent the easiest
way to start development on MS Windows.

.. _Python 3 installer: https://www.python.org/downloads/
.. _git for Windows: https://gitforwindows.org/


Mac OS X
^^^^^^^^

Download the `official installer`_ and install Python 3 by executing .pkg file.
Finally, run provided post-install script **Install Certificates.command**.

.. _official installer: https://www.python.org/downloads/


Python requirements
-------------------

You should develop **arrangeit** in a dedicated virtual environment. If you don't
have any other preferred way, then probably the easiest way to create a virtual
environment would be **venv** integrated with Python 3.5+.

For example, if you place your projects in ``projects`` directory and path to
arrangeit root directory is ``/home/yourusername/projects/arrangeit`` (or
``c:\Users\yourusername\projects\arrangeit`` on MS Windows), then you may create
a directory inside projects directory to hold your virtual environments.

.. code-block:: bash

  $ cd ~/projects
  $ mkdir venvs
  $ cd venvs


Create a new virtual environment with:

.. code-block:: bash

  $ python3 -m venv arrangeit


The virtual environment is activated on GNU/Linux from ``venvs`` directory with:

.. code-block:: bash

  $ source arrangeit/bin/activate


Or in MS Windows with:

.. code-block::

  arrangeit\Scripts\activate.bat


Install the base requirements by issuing the following from the project's root
directory:

.. code-block:: bash

  (arrangeit) $ python -m pip install -U -r requirements/linux.txt


And all the necessary Python dependency packages for **arrangeit** development with:

.. code-block:: bash

  (arrangeit) $ python -m pip install -U -r requirements/base_development.txt


Additional tools
----------------

pygettext
^^^^^^^^^

**pygettext** is a Python wrapper for *xgettext* and it ships with Python. To prepare
translation template, run the following command on Ubuntu from the project's root
directory:

.. code-block:: bash

  find ./arrangeit -iname "*.py" | xargs pygettext3 --verbose --extract-all \
    --default-domain=arrangeit --output-dir=./arrangeit/locale


Create a language_ directory inside ``locale`` directory, and inside that language
directory create another directory with the name ``LC_MESSAGES``. Finally, copy
arrangeit translation template into that directory and rename it to ``arrangeit.po``.

Here's how it was done from the project's root directory for the Croatian language:

.. code-block:: bash

  $ mkdir -p arrangeit/locale/hr_HR/LC_MESSAGES
  $ cp arrangeit/locale/arrangeit.pot arrangeit/locale/hr_HR/LC_MESSAGES/arrangeit.po

If an existing translation needs to be updated after ``arrangeit.pot`` has been
changed, then you should update the differences with **msgmerge**:

.. code-block:: bash

  $ msgmerge --update arrangeit/locale/hr_HR/LC_MESSAGES/arrangeit.po arrangeit/locale/arrangeit.pot


After the translation is finished, compile the language file with **msgfmt**:

.. code-block:: bash

  $ cd arrangeit/locale/hr_HR/LC_MESSAGES
  $ msgfmt -o arrangeit.mo arrangeit.po


If you use Poedit_ for translation, then instead of the last command you may create
compiled file by clicking the Save button in Poedit.


.. _language: https://www.gnu.org/software/gettext/manual/html_node/Locale-Names.html
.. _Poedit: https://poedit.net/


black
^^^^^

Any code should be formatted by **black** before commit.

It should have been installed together with other development requirements
(``python -m pip install -r requirements/base_development.txt``) or you may
install it separately with:

.. code-block:: bash

  $ python3 -m pip install black


Run it from the root directory by:

.. code-block:: bash

  $ black arrangeit


pyflakes
^^^^^^^^

Install **pyflakes** linter with:

.. code-block:: bash

  $ python3 -m pip install pyflakes


Run it from the project's root directory by:

.. code-block:: bash

  $ python3 -m pyflakes arrangeit


py2deb
^^^^^^

py2deb_ is used to build GNU/Linux installation package.

.. _py2deb: https://py2deb.readthedocs.io


Run the following command to install py2deb and its dependencies on Debian/Ubuntu:

.. code-block:: bash

  $ sudo apt-get install dpkg-dev fakeroot lintian python3-pip
  $ pip3 install py2deb --user
  $ pip3 install pip-accel --user  # it will downgrade pip to version <8.0


And then run the following command inside the project's root directory to create
Debian installation package in `./dist/` directory:

.. code-block:: bash

  $ mkdir dist
  $ py2deb -r ./dist/ --no-name-prefix=arrangeit -y \
      --use-system-package=Pillow,python3-pil \
      --use-system-package=python-xlib,python3-xlib \
      --use-system-package=six,python3-six \
      .


PyInstaller
^^^^^^^^^^^

PyInstaller_ is used to build MS Windows installation package.

.. _PyInstaller: https://www.pyinstaller.org/

`starter.py` script is created in the project's root directory for the purpose of
PyInstaller's dependencies collecting. The specification file ``pyinstaller.spec``
in the same directory is used to produce MS Windows executable by the following call:

.. code-block:: bash

  (arrangeit) $ python -OO -m PyInstaller pyinstaller.spec


SonarQube
^^^^^^^^^

SonarQube_ is an open-source platform for inspection of code quality for detecting
bugs, code smells, and security vulnerabilities.

.. _SonarQube: https://docs.sonarqube.org/latest/setup/get-started-2-minutes/


Starting server
"""""""""""""""

.. code-block:: bash

  $ ~/opt/repos/sonarqube-7.7/bin/linux-x86-64/sonar.sh console


Starting scanner
""""""""""""""""

You should add scanner executable to your PATH. For example, by adding the following
line to your ``~/.bashrc``:

.. code-block:: bash

  export PATH=$PATH:~/opt/repos/sonar-scanner/bin


To start scanning, run the scanner from the root directory of the project with:

.. code-block:: bash

  $ sonar-scanner

For additional information read the scanner `documentation`_.

.. _documentation: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/


Administration
""""""""""""""

Prepare coverage's XML report by running the following in the project's root
directory:

.. code-block:: bash

  (arrangeit) $ python -m pytest -v --cov-report xml:tests/coverage-linux.xml --cov=arrangeit


Overview
""""""""

Open your browser and point it to http://localhost:9000. Login as **admin/admin**.
