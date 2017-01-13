.. _first_project:

First own project
=================
In this chapter we will create our first project, start our first application and
add new plugins to the application to enhance its functionality.

Using recipes
--------------
Luckily we do not need to create even one single file by hand.

groundwork knows project templates, called recipes, and we will use one of them to set up our first project.

List all known recipes
~~~~~~~~~~~~~~~~~~~~~~
Lets find out, which recipes are available in groundwork itself::

    >>> groundwork recipe_list
    Recipes:
      gw_package by plugin 'GwRecipesBuilder' - Groundwork basic package. Includes places for apps, plugins, patterns and recipes.

groundwork provides only one recipe, called ``gw_package``, which contains everything we need for a fast project setup.

Use gw_package recipe
~~~~~~~~~~~~~~~~~~~~~~
*"That's one small step for you, one giant leap for your project"* or something similar Armstrong has already told us.
So, lets start the build of the recipe::

    >>> groundwork recipe_build gw_package
    full_name [My Name]: Team Awesome
    github_user [team_awesome]:
    email [team_awesome@provider.com]:
    project_name [My Package]: CSV-Manager
    project_slug [csv_manager]:
    github_project_name [csv-manager]:
    project_app [csv_manager_app]:
    project_plugin [csv_manager_plugin]:
    project_short_description [Package for hosting groundwork apps and plugins like csv_manager_app or csv_manager_plugin.]:
    test_folder [tests]:
    test_prefix [test_]:
    version [0.1.0]:
    Select license:
    1 - MIT license
    2 - BSD license
    3 - ISC license
    4 - Apache Software License 2.0
    5 - GNU General Public License v3
    6 - Not open source
    Choose from 1, 2, 3, 4, 5, 6 [1]: 1

    Recipe Installation is done.

    During development use buildout:
    Run: python bootstrap.py
    Then: bin/buildout
    Start the app: bin/app

    For installation run: 'python setup.py install'
    For documentation run: 'make html' inside doc folder (after installation!)

    For more information, please take a look into the README file to know how to go on.
    For help visit: https://groundwork.readthedocs.io

    Have fun with your groundwork package.

As you see, you will get asked some questions during the build. The answers are used to name directories and files or to
write related data into some files.

For each question, groundwork provides a proposal. Just press ENTER to accept this as input.

Please answer the questions as followed:

| full_name: **Team Awesome**
| github_user: **ENTER**
| email: **ENTER**
| project_name: **CSV-Manager**
| project_slug: **ENTER**  # IMPORTANT: No minus in name!
| github_project_name: **ENTER**
| project_app: **ENTER**
| project_plugin: **ENTER**
| project_short_description: **ENTER**
| test_folder: **ENTER**
| test_prefix: **ENTER**
| version: **ENTER**
| Select license: **ENTER**


The output should look like the above example.

.. note::
   For more information about recipes read the
   `technical documentation about recipes <https://groundwork.readthedocs.io/en/latest/recipes.html>`_.

Project content
---------------

Lets take a look into the newly created folder ``CSV-Manager``::

   >>> cd CSV-Manager
   >>> tree --dirsfirst  # linux command
   .
   ├── csv_manager
   │   ├── applications
   │   │   ├── configuration.py
   │   │   ├── csv_manager_app.py
   │   │   └── __init__.py
   │   ├── patterns
   │   │   └── __init__.py
   │   ├── plugins
   │   │   ├── csv_manager_plugin.py
   │   │   └── __init__.py
   │   ├── recipes
   │   │   └── __init__.py
   │   ├── __init__.py
   │   └── version.py
   ├── docs
   │   ├── _static
   │   │   ├── gw_logo.png
   │   │   └── gw_slogan.png
   │   ├── conf.py
   │   ├── index.rst
   │   └── Makefile
   ├── tests
   │   ├── __init__.py
   │   └── test_app.py
   ├── bootstrap.py
   ├── buildout.cfg
   ├── doc-requirements.txt
   ├── README
   ├── setup.py
   ├── test-requirements.txt
   ├── tox.ini
   └── versions.cfg


Code structure
~~~~~~~~~~~~~~

You will find all important python code inside the folder ``csv_manager``, which is a normal, importable python package.

Inside this package there are 4 sub-packages: ``applications``, ``patterns``, ``plugins`` and ``recipes``.
Currently only ``applications`` and ``plugins`` have some content. All others are not used yet.

There is also one ``setup.py`` file on the root level of your project.
This file stores all your project meta data and is used by ``pip`` to install your project.
It is also responsible for registering plugins in the python environment during installation.

Application: csv_manager_app.py
+++++++++++++++++++++++++++++++
Lets take a look into the application. Open `csv_manager_app.py`:

.. literalinclude:: /../../code/chapter_1/01_first_project/CSV-Manager/csv_manager/applications/csv_manager_app.py
   :language: python
   :linenos:

The most important part is between line 14-16. There we create our groundwork App object [14] and tell the app, which
plugins shall be activated [15]. Finally we start the command line interface to interact with the user [16].

The lines 3 and 10+11 are responsible for creating the working directory of our App, which is defined as ``APP_PATH``
in the configuration file.

Configuration files were provided to the App during class initialisation [12].

Application configuration
+++++++++++++++++++++++++

Now take a look into the configuration file ``configuration.py``:

.. literalinclude:: /../../code/chapter_1/01_first_project/CSV-Manager/csv_manager/applications/configuration.py
   :language: python
   :linenos:

Line 10 to end is all about configuring the python logging. If you want to change the layout of the log messages,
the logging level or the logging destination, this is the place to make changes.

However the most important configuration parameters are ``APP_NAME``, ``APP_PATH`` and ``PLUGINS``.

``APP_NAME`` is used to give your application a meaningful name in documentation and interfaces.

``APP_PATH`` can be used by plugins to store some specific data into it. For example the default logging configuration
stores a debug log into it (see line 32).

And ``PLUGINS`` defines a list of plugins, which shall be loaded and activated during application start up.
We will add some additional plugins in a few moments.

Plugin: csv_manager_plugin.py
+++++++++++++++++++++++++++++

Finally lets take a look into our plugin ``csv_manager_plugin.py``:

.. literalinclude:: /../../code/chapter_1/01_first_project/CSV-Manager/csv_manager/plugins/csv_manager_plugin.py
   :language: python
   :linenos:

Our plugin will register a command for the command line interface,
therefore we need the pattern ``GwCommandsPattern`` [1].

Line 4 shows us the definition of your class, which inherits from ``GwCommandsPattern``.

Inside the ``__init__`` routine [5-7] we give our plugin a name. In this case it is the class name.
The used GwCommandsPattern has also an own ``__init__`` routine and we must be sure that this gets also called [7].

Each plugin must have a ``activate`` and ``deactivate`` function. They get called, if a plugin is going to be
activated or deactivated.

In our ``activation`` routine a command is registered [10].
``self.commands.register`` is available, because our plugin inherits from ``GwCommandsPattern``.
Other patterns would provide other functions, like ``self.documents.get()`` when using the ``GwDocumentsPattern``.

.. note::
   A plugin can inherit from as much patterns as it likes.

   Pattern-Inheritance is the default way in groundwork to enhance your plugin with useful and time-saving functions
   during development.

Documentation
~~~~~~~~~~~~~

Beside the code, our groundwork package also contains a ready-to-use sphinx documentation project.

You can find it in ``/docs`` and you are free to generate it::

   >>> cd docs
   >>> make html
   sphinx-build -b html -d _build/doctrees   . _build/html
   Running Sphinx v1.5.1
   making output directory...
   Getting latest version of groundwork sphinx theme
     Checking for gitpython library... done
     Checking for working internet connection... done
     Getting latest theme updates... done
   loading pickled environment... not yet created
   building [mo]: targets for 0 po files that are out of date
   building [html]: targets for 2 source files that are out of date
   updating environment: 2 added, 0 changed, 0 removed
   reading sources... [100%] index
   looking for now-outdated files... none found
   pickling environment... done
   checking consistency... done
   preparing documents... done
   writing output... [100%] index
   generating indices... genindex
   writing additional pages... search
   copying images... [100%] _themes/screenshot.png
   copying static files... WARNING: logo file '/_static/gw_logo.png' does not exist
   done
   copying extra files... done
   dumping search index in English (code: en) ... done
   dumping object inventory... done
   build succeeded, 2 warnings.

You can open the generated html website in any browser. Just open ``_build/html/index.html``.

.. figure:: /_static/sphinx_initial_doc_screenshot.png

   Generated documentation website of a fresh created groundwork project

Looks awesome? Read :ref:`sphinx` for more awesomeness.

Tests
~~~~~

Your project has also a preconfigured test-environment with a test example::

   >>> cd tests
   >>> tree  # linux command
   ├── __init__.py
   └── test_app.py

Lets take a look into the test file ``test_app``:

.. literalinclude:: /../../code/chapter_1/01_first_project/CSV-Manager/tests/test_app.py
   :language: python
   :linenos:

groundwork uses :ref:`pytest` for its tests. The important tests are done in the line with ``assert`` in it (3, 14, 15).

To run the tests simply execute the following::

   >>> cd tests
   >>> pytest
   ==================== test session starts =====================
   platform linux -- Python 3.5.2, pytest-3.0.5, py-1.4.32, pluggy-0.4.0
   rootdir: /.../groundwork-tutorial/code/chapter_1/01_first_project/CSV-Manager, inifile: tox.ini
   collected 2 items

   test_app.py ..

   ================== 2 passed in 0.28 seconds ===================

The tests will fail, if the CSV-Manager is not installed. Which should be the case right now.

Instead of :ref:`pytest` you could also use :ref:`tox`, which cares about correct installation and can run your tests
with different configurations (e.g. with Python 3.4 and Python 3.5).

:ref:`tox` is also preconfigured to use FLAKE8, which checks your coding styles, and to generate a coverage report::

   >>> cd tests
   >>> tox
   GLOB sdist-make: /.../groundwork-tutorial/code/chapter_1/01_first_project/CSV-Manager/setup.py
   py34 create: /.../groundwork-tutorial/code/chapter_1/01_first_project/CSV-Manager/.tox/py34
   ERROR: InterpreterNotFound: python3.4
   py35 inst-nodeps: /.../groundwork-tutorial/code/chapter_1/01_first_project/CSV-Manager/.tox/dist/csv_manager-0.1.0.zip
   py35 installed: alabaster==0.7.9,arrow==0.10.0,Babel==2.3.4,binaryornot==0.4.0,blinker==1.4,chardet==2.3.0,click==6.7,cookiecutter==1.5.0,coverage==4.3.1,csv-manager==0.1.0,docutils==0.13.1,flake8==3.2.1,future==0.16.0,gitdb2==2.0.0,GitPython==2.1.1,groundwork==0.1.5,imagesize==0.7.1,Jinja2==2.9.4,jinja2-time==0.2.0,MarkupSafe==0.23,mccabe==0.5.3,poyo==0.4.0,py==1.4.32,pycodestyle==2.2.0,pyflakes==1.3.0,Pygments==2.1.3,pytest==3.0.5,pytest-flake8==0.8.1,pytest-runner==2.9,python-coveralls==2.9.0,python-dateutil==2.6.0,pytz==2016.10,PyYAML==3.12,requests==2.12.4,six==1.10.0,smmap2==2.0.1,snowballstemmer==1.2.1,Sphinx==1.5.1,whichcraft==0.4.0
   py35 runtests: PYTHONHASHSEED='1116081422'
   py35 runtests: commands[0] | coverage run --source csv_manager -m py.test --flake8
   ==================================== test session starts =====================================
   platform linux -- Python 3.5.2, pytest-3.0.5, py-1.4.32, pluggy-0.4.0
   rootdir: /.../groundwork-tutorial/code/chapter_1/01_first_project/CSV-Manager, inifile: tox.ini
   plugins: flake8-0.8.1
   collected 16 items

   __init__.py s
   setup.py s
   csv_manager/__init__.py s
   csv_manager/version.py s
   csv_manager/applications/__init__.py s
   csv_manager/applications/configuration.py s
   csv_manager/applications/csv_manager_app.py s
   csv_manager/patterns/__init__.py s
   csv_manager/plugins/__init__.py s
   csv_manager/plugins/csv_manager_plugin.py s
   csv_manager/recipes/__init__.py s
   docs/conf.py s
   tests/__init__.py s
   tests/test_app.py s..

   ============================ 2 passed, 14 skipped in 0.21 seconds ============================
   py35 runtests: commands[1] | coverage report
   Name                                          Stmts   Miss  Cover
   -----------------------------------------------------------------
   csv_manager/__init__.py                           0      0   100%
   csv_manager/applications/__init__.py              1      0   100%
   csv_manager/applications/configuration.py         7      0   100%
   csv_manager/applications/csv_manager_app.py      15      5    67%
   csv_manager/patterns/__init__.py                  0      0   100%
   csv_manager/plugins/__init__.py                   1      0   100%
   csv_manager/plugins/csv_manager_plugin.py         9      1    89%
   csv_manager/recipes/__init__.py                   0      0   100%
   csv_manager/version.py                            1      1     0%
   -----------------------------------------------------------------
   TOTAL                                            34      7    79%
   __________________________________________ summary ___________________________________________
   ERROR:   py34: InterpreterNotFound: python3.4
     py35: commands succeeded

Install and run our project
---------------------------

It's time for installing our CSV-Manager and start working and coding with it::

    >>> cd CSV-Manager
    >>> pip install -e .
    # A lot of output

This will install the CSV-Manager inside the current Python environment.

By using the option ``-e`` no files will be copied, instead pip sets some links to our code.
This allows us to make changes to the code without the need of reinstallation.

And finally::

    >>> csv_manager
    2017-01-13 09:55:24,533 - INFO  - Application signals initialised
    2017-01-13 09:55:24,715 - INFO  - Application commands initialised
    2017-01-13 09:55:24,716 - INFO  - Plugins initialised: csv_manager_plugin
    2017-01-13 09:55:24,716 - INFO  - Application documents initialised
    2017-01-13 09:55:24,716 - INFO  - Plugins initialised: GwPluginsInfo
    2017-01-13 09:55:24,717 - INFO  - Plugins activated: csv_manager_plugin, GwPluginsInfo
    Usage: csv_manager [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      hello_world  Prints hello world
      plugin_list  List all plugins

Yeah, our app is running and the plugin ``csv_manager_plugin`` has already registered a command.
Execute it with::

   >>> csv_manager hello_world
   2017-01-13 17:12:11,857 - INFO  - Application signals initialised
   2017-01-13 17:12:12,039 - INFO  - Application commands initialised
   2017-01-13 17:12:12,039 - INFO  - Plugins initialised: csv_manager_plugin
   2017-01-13 17:12:12,040 - INFO  - Application documents initialised
   2017-01-13 17:12:12,040 - INFO  - Plugins initialised: GwPluginsInfo
   2017-01-13 17:12:12,041 - INFO  - Plugins activated: csv_manager_plugin, GwPluginsInfo
   Hello World. It's me, csv_manager_plugin!

Enhance application
-------------------

It's time for pimping our app. All we need is to load additional plugins...

Add document viewer
~~~~~~~~~~~~~~~~~~~
Open ``csv_manager/applications/configuration.py`` and add the plugin ``GwDocumentsInfo`` to the plugins list::

    # PLUGINS = ["csv_manager_plugin", "GwPluginsInfo"]  # Old config
    PLUGINS = ["csv_manager_plugin", "GwPluginsInfo", "GwDocumentsInfo"]  # New config

Run ``csv_manager`` again::

    >>> csv_manager
    2017-01-13 10:04:53,729 - INFO  - Application signals initialised
    2017-01-13 10:04:53,925 - INFO  - Application commands initialised
    2017-01-13 10:04:53,925 - INFO  - Plugins initialised: csv_manager_plugin
    2017-01-13 10:04:53,926 - INFO  - Application documents initialised
    2017-01-13 10:04:53,926 - INFO  - Plugins initialised: GwPluginsInfo
    2017-01-13 10:04:53,927 - INFO  - Plugins initialised: GwDocumentsInfo
    2017-01-13 10:04:53,928 - INFO  - Plugins activated: csv_manager_plugin, GwPluginsInfo, GwDocumentsInfo
    Usage: csv_manager [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      doc          Shows the documentation
      doc_list     List all documents
      doc_write    Stores documents as files
      hello_world  Prints hello world
      plugin_list  List all plugins

You got three new commands by just adding the related plugin ``GwDocumentsInfo`` to your config.


Add web interface
~~~~~~~~~~~~~~~~~

.. Note::
   For this example the python package ``groundwork-web`` must be installed.
   You can do this easily with ``pip install groundwork-web``.

Lets do one last example to show you how powerful your application can become by just adding plugins.

Again open ``csv_manager/applications/configuration.py`` and add the plugin ``GwWeb`` and ``GwWebManager`` to the
plugin list::

    # PLUGINS = ["csv_manager_plugin", "GwPluginsInfo", "GwDocumentsInfo"]  # Old config
    PLUGINS = ["csv_manager_plugin", "GwPluginsInfo", "GwDocumentsInfo", "GwWeb", "GwWebManager"]  # New config

Run ``csv_manager`` again::

    >>> csv_manager
    2017-01-13 10:10:35,117 - INFO  - Application signals initialised
    2017-01-13 10:10:35,315 - INFO  - Application commands initialised
    2017-01-13 10:10:35,315 - INFO  - Plugins initialised: csv_manager_plugin
    2017-01-13 10:10:35,315 - INFO  - Application documents initialised
    2017-01-13 10:10:35,316 - INFO  - Plugins initialised: GwPluginsInfo
    2017-01-13 10:10:35,316 - INFO  - Plugins initialised: GwDocumentsInfo
    2017-01-13 10:10:35,317 - INFO  - Plugins initialised: GwWeb
    2017-01-13 10:10:35,319 - INFO  - Using FLASK_SERVER_NAME=127.0.0.1:5000
    2017-01-13 10:10:35,319 - INFO  - Route registered:  /test for context web (/)
    2017-01-13 10:10:35,320 - INFO  - Plugins initialised: GwWebManager
    2017-01-13 10:10:35,320 - INFO  - Route registered:  / for context webmanager (/webmanager)
    2017-01-13 10:10:35,320 - INFO  - Route registered:  /command for context webmanager (/webmanager)
    2017-01-13 10:10:35,321 - INFO  - Route registered:  /plugin for context webmanager (/webmanager)
    2017-01-13 10:10:35,321 - INFO  - Route registered:  /plugin/class/<clazz> for context webmanager (/webmanager)
    2017-01-13 10:10:35,321 - INFO  - Route registered:  /plugin/instance/<plugin_name> for context webmanager (/webmanager)
    2017-01-13 10:10:35,322 - INFO  - Route registered:  /signal for context webmanager (/webmanager)
    2017-01-13 10:10:35,322 - INFO  - Route registered:  /receiver for context webmanager (/webmanager)
    2017-01-13 10:10:35,322 - INFO  - Route registered:  /document for context webmanager (/webmanager)
    2017-01-13 10:10:35,323 - INFO  - Route registered:  /route for context webmanager (/webmanager)
    2017-01-13 10:10:35,323 - INFO  - Route registered:  /menu for context webmanager (/webmanager)
    2017-01-13 10:10:35,324 - INFO  - Route registered:  /context for context webmanager (/webmanager)
    2017-01-13 10:10:35,324 - INFO  - Route registered:  /server for context webmanager (/webmanager)
    2017-01-13 10:10:35,325 - INFO  - Plugins activated: csv_manager_plugin, GwPluginsInfo, GwDocumentsInfo, GwWeb, GwWebManager
    Usage: csv_manager [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      doc           Shows the documentation
      doc_list      List all documents
      doc_write     Stores documents as files
      hello_world   Prints hello world
      plugin_list   List all plugins
      server_list   prints a list of registered server
      server_start  starts a given server

Ohh nice, we got commands to start a webserver. Lets do it::

    >>> csv_manager server_start flask_debug
    2017-01-13 10:11:44,562 - INFO  - Application signals initialised
    2017-01-13 10:11:44,745 - INFO  - Application commands initialised
    2017-01-13 10:11:44,745 - INFO  - Plugins initialised: csv_manager_plugin
    2017-01-13 10:11:44,746 - INFO  - Application documents initialised
    2017-01-13 10:11:44,746 - INFO  - Plugins initialised: GwPluginsInfo
    2017-01-13 10:11:44,747 - INFO  - Plugins initialised: GwDocumentsInfo
    2017-01-13 10:11:44,748 - INFO  - Plugins initialised: GwWeb
    2017-01-13 10:11:44,749 - INFO  - Using FLASK_SERVER_NAME=127.0.0.1:5000
    2017-01-13 10:11:44,749 - INFO  - Route registered:  /test for context web (/)
    2017-01-13 10:11:44,750 - INFO  - Plugins initialised: GwWebManager
    2017-01-13 10:11:44,751 - INFO  - Route registered:  / for context webmanager (/webmanager)
    2017-01-13 10:11:44,751 - INFO  - Route registered:  /command for context webmanager (/webmanager)
    2017-01-13 10:11:44,751 - INFO  - Route registered:  /plugin for context webmanager (/webmanager)
    2017-01-13 10:11:44,752 - INFO  - Route registered:  /plugin/class/<clazz> for context webmanager (/webmanager)
    2017-01-13 10:11:44,752 - INFO  - Route registered:  /plugin/instance/<plugin_name> for context webmanager (/webmanager)
    2017-01-13 10:11:44,752 - INFO  - Route registered:  /signal for context webmanager (/webmanager)
    2017-01-13 10:11:44,753 - INFO  - Route registered:  /receiver for context webmanager (/webmanager)
    2017-01-13 10:11:44,753 - INFO  - Route registered:  /document for context webmanager (/webmanager)
    2017-01-13 10:11:44,754 - INFO  - Route registered:  /route for context webmanager (/webmanager)
    2017-01-13 10:11:44,754 - INFO  - Route registered:  /menu for context webmanager (/webmanager)
    2017-01-13 10:11:44,754 - INFO  - Route registered:  /context for context webmanager (/webmanager)
    2017-01-13 10:11:44,755 - INFO  - Route registered:  /server for context webmanager (/webmanager)
    2017-01-13 10:11:44,756 - INFO  - Plugins activated: csv_manager_plugin, GwPluginsInfo, GwDocumentsInfo, GwWeb, GwWebManager
    Starting server flask_debug
    2017-01-13 10:11:44,756 - INFO  - Flask Server Name: 127.0.0.1:5000
    2017-01-13 10:11:44,764 - INFO  -  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

So we got a running webserver and therefore there should be an available website.

Open a browser and visit http://127.0.0.1:5000/webmanager/. You should see a page looking like this:

.. figure:: /_static/webmanager_screenshot.png

   Overview web page of the plugin **WebManager**

.. note::
   There is a whole chapter :ref:`chapter_3`, which cares about the topic web and lets you create your own web plugin.

Cleaning up
~~~~~~~~~~~

For the next chapters, we do not need the just added plugins. If you like you can edit
``csv_manager/applications/configuration.py`` and remove not needed plugins::

   PLUGINS = ["csv_manager_plugin", "GwPluginsInfo"]

Great, we are done with this chapter. Ready for python coding and creating your own plugin?
Go on with :ref:`first_plugin`.

