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


Darwin
^^^^^^

Download official installer from https://www.python.org/downloads/, download and install Python by executing .pkg file 
and finally run post-install script `Install Certificates.command`.


Tools
-----

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