.. _installation:

Installation
============

Virtual Environment
-------------------

Before we will install groundwork, it would be great if we had a fresh and untouched Python installation.
Luckily it is not necessary to do a complete new installation, because Python supports virtual environments.

These virtual environments are based on an already installed Python installation, but all additional
installed packages not visible within the virtual environment.

.. note::
   groundwork supports Python >3.4 only. Please make sure your installed Python Environment is correct.

Creation
~~~~~~~~
To create a new virtual environment, execute the following on the commandline::

    python3 -m venv gw_venv

This will create the virtual environment ``gw_venv`` (groundwork virtual environment) in the folder
``gw_venv`` of the current working directory.

Activation
~~~~~~~~~~
To activate your new virtual environment, execute one of the following commands::

    source gw_venv/bin/activate  # For Linux
    gw_venv\Scripts\activate.bat # For Windows

After that, the prefix ``(gw_venv)`` should show up in front of your command prompt.

groundwork Installation
-----------------------

After activating your new virtual environment, we simply use ``pip`` to install groundwork::

    pip install groundwork

The virtual environment version of pip is used which installs groundwork to the virtual environment.

Alternative: Installation from source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you want a installation from the latest groundwork source code, you need to clone the project repository
and perform a development installation::

    git clone https://github.com/useblocks/groundwork
    cd groundwork
    pip install -e .

``pip install -e .`` sets only links from the source code to the used virtual environment.
So changes on the code are directly available without any reinstallation (except if you have changed ``setup.py`` ).

Packages for test execution and documentation building
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For a normal user the just installed packages are enough to run groundwork and all related applications.

However, developers normally want also to run tests and maybe generate the documentation by their own.
For this tasks additional python packages are needed, which are not needed for normal usage.
Therefore these package are not part of the normal installation and must be installed by the developers.

Luckily these dependencies are also collected in one single file, so that it can be used as input for ``pip``.
Let's install these packages to be prepared::

    pip install -r docs/doc-requirements.txt
    pip install -r code/test-requirements.txt

Tests
-----

Finally let's check if groundwork was installed correctly, by trying to execute the command ``groundwork``::

    >>> groundwork
    Usage: groundwork [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      doc            Shows the documentation
      doc_list       List all documents
      doc_write      Stores documents as files
      plugin_list    List all plugins
      receiver_list  List of all signal receivers
      recipe_build   Builds a given recipe
      recipe_list    Lists all recipes
      signal_list    List of all signals

If you see the above output, congratulation!
groundwork is installed and we can go on to examine the ``groundwork`` command in the chapter :ref:`usage`.
