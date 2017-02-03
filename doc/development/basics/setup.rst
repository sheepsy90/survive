.. _setup_survive:

First Time Setup of the Survive Project
=======================================

.. hint:: 

  The following instruction applies to users of a Debian based System like Ubuntu.


1. Step - Preconditions
-----------------------
To productively program survive you should have:

* Linux-System
* Make sure your Public-Key is registered in the git

2. Step - Git
-------------

When you made sure that you have given your public key to the correct person,
you should be able to perform the following command:

  git clone gitolite@heleska.de:survive [destination]

This creates a subfolder which contains the complete survive project.

.. hint::

  If you don't provide a *destination* the folder will be named "survive".

3. Step - Set up the Virtualenv
-------------------------------

If you change to the created directory you should find a command which sets up the virtualenv.
This is a specific environment that can be activated in which all necessary libraries are included and
contained such that they don't interfere with your system.

In general to setup the virtualenv you can execute:

  sudo ./setup_virtual_env.sh

This creates a virtualenv in the *.game* folder. To start the system locally you will need to activate
the virtualenv. You can do this with:

  . .game/bin/activate

4. Step - Get it all up and running
-----------------------------------

.. todo::
    Explain how the system is started.

