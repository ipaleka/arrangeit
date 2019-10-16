Functional testing
==================

System requirements
-------------------

VirtualBox
^^^^^^^^^^

**arrangeit** functional testing is done inside a VirtualBox virtual machine
created with Vagrant. In Ubuntu, you may install VirtualBox by issuing the
following command:

.. code-block:: bash

  $ sudo apt-get install virtualbox virtualbox-guest-utils \
      virtualbox-guest-x11 virtualbox-guest-dkms


Vagrant
^^^^^^^

Vagrant may be downloaded from:

https://www.vagrantup.com/downloads.html

In Ubuntu, install downloaded package with:

.. code-block:: bash

  $ sudo dpkg -i vagrant_2.2.5_x86_64.deb


Ansible
^^^^^^^

You may install Ansible in ubuntu

.. code-block:: bash

  $ sudo apt-get install ansible


Another way is installation by `pip` for the current user:

.. code-block:: bash

  $ pip install ansible --upgrade --user


Memory and disk space requirements
----------------------------------

2GB of RAM is assigned to a virtual machine in the arrangeit `Vagrantfile`
located in `tests/vm` subdirectory.

A virtual machine will occupy approximately 10GB of disk space upon finished
installation, together with the size of related Vagrant box/image.

So in the case of three virtual machines you should have available at least
6GB of RAM and 30GB of disk space if you want to test them all at once. For
testing one virtual machine at a time you'll need 2GB of RAM and 10GB of disk
space.


Running tests
-------------

Robot Framework functional tests for arrangeit will run automatically
for every Vagrant virtual machine if you invoke the following command
from the `tests/vm` directory:

.. code-block:: bash

  $ vagrant up


That command will - in serial for all defined Vagrant machines - download
the Vagrant box if it isn't already downloaded, install the OS in an idempotent
way and finally run the Robot Framework functional tests for arrangeit.

Run the same command with added virtual machine name if you want to run tests
for a single virtual machine:

.. code-block:: bash

  $ vagrant up xfcevm


If the provision phase has failed or you've updated some provisioning ansible
task, then you may re-initiate provisioning with:

.. code-block:: bash

  $ vagrant up --provision xfcevm


Invoke the following command in order to remove the virtual machine completely:

.. code-block:: bash

  $ vagrant destroy xfcevm


If you omit the virtual machine name in the last two commands then all
virtual machines will be affected.
