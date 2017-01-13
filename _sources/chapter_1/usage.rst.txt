.. _usage:

Usage
=====

.. note::
   For the following steps groundwork must be installed.

   If not done yet, please follow :ref:`installation`.

In the last chapter :ref:`installation` you may have already noticed that groundwork has its own little execution
command. groundwork tries to help you as early as possible inside your personal development process.

This means it is not only focused on providing functions for your code.
It can also help you with setting up new projects or analysing and understanding existing projects.

But lets start with the basics by calling it::

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

Calling groundwork without any parameters will show you the above help message.
As you can see, you get a nice list of available commands.

If you need more information to a specific command, execute ``groundwork <command> --help``. Example::

   >>> groundwork doc_write --help
   Usage: groundwork doc_write [OPTIONS] PATH

     Stores documents as files

   Options:
     -h, --html       Will output html instead of rst
     -o, --overwrite  Will overwrite existing files
     -q, --quiet      Will suppress any user interaction
     --help           Show this message and exit.

Real-time documentation
-----------------------
Plugins are allowed to register documents, which can contain static text or dynamic information like currently active
plugins.

Because the command `groundwork` starts itself a groundwork based application, we can easily examine this application
by taking a look into the registered documents::

   >>> groundwork doc
   groundwork basic app
   ====================

   Application overview
   --------------------

   Path: /.

   Active plugins: 5

   Registered commands: 8

   Registered signals: 4
   Registered receivers: 10

   Registered documents: 7

   ---------------------------------------------------------------------------
   This document is registered by 'groundwork basic app' under the name 'main'
   ---------------------------------------------------------------------------
   Actions: [N]ext, E[x]it
   Select your action [N]:

This starts a console based document viewer and you can use the keys **N** and **P** + **ENTER**
to see next or previous chapter.
To exit just type **x** and press **ENTER**

In one of the last lines you see which plugin has registered the currently showed document and you see the internal,
unique document name.

You will find documents for registered commands, signals or plugins.

The page ``plugin_classes`` shows you an overview about all registered plugins inside the currently used
Python Environment. This means each groundwork application could use this plugins by just adding their names to
its config. We will do this in the next chapter :ref:`first_project`.

To get an overview about all used plugins by the current application, open the page ``plugins_overviews``.

Documents are supporting RST and Jinja and therefore can be easily transformed to any kind of presentation.
You can view them on console, export them to sphinx or read them on a webpage.
And documents are always up to date, as their content is mostly calculated during runtime.

Exporting documents
~~~~~~~~~~~~~~~~~~~

The ``GwDocumentInfo`` plugin has registerd a command, which exports and stores documents on a hard disk.

Lets say we want the documents as RST output in the folder temp::

   >>> mkdir temp
   >>> groundwork doc_write -h temp
   Storing groundwork application documents

   Application: groundwork basic app
   Number of documents: 7

   Going to write to following files:
     signals_overview.rst
     main.rst
     plugins_classes.rst
     documents_overview.rst
     plugins_overview.rst
     receivers_overview.rst
     commands_overview.rst

   Target directory: /.../temp
   Shall we go on? [Y]es, [N]o: : y
   signals_overview.rst stored.
   main.rst stored.
   plugins_classes.rst stored.
   documents_overview.rst stored.
   plugins_overview.rst stored.
   receivers_overview.rst stored.
   commands_overview.rst stored.


As you can see, for each virtual document a rst file was created::

   >>> tree temp  # linux command
   temp
   ├── commands_overview.rst
   ├── documents_overview.rst
   ├── main.rst
   ├── plugins_classes.rst
   ├── plugins_overview.rst
   ├── receivers_overview.rst
   └── signals_overview.rst

That's it. On the next chapter we will use the ``recipe_build`` command to create our first own groundwork project.
Go on with :ref:`first_project`.
