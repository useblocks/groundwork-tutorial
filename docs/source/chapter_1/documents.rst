.. _documents:

Using configs and documents
===========================

In this chapter we will learn how to get access on the application configuration,
create a second plugin, which will archive csv changes and show them inside a groundwork document.

Using the config
----------------
Right now our plugin ``CsvWathcerPlugin`` only monitors a file, if the user has requested this by calling the related
command ``csv_watch``.

Let's add the possibility to define a list of files in the configuration, which shall always be monitored.

Open ``csv_watcher_plugin.py`` and add the following code at the end of the ``activation()`` routine::

    csv_files_by_config = self.app.config.get("CSV_FILES", [])
    csv_interval_by_config = self.app.config.get("CSV_INTERVAL", 5)

    for csv_file in csv_files_by_config:
        self.csv_watcher_command(csv_file, csv_interval_by_config

In the first two lines we requested two configuration values. For the case that a requested
configuration parameter is not available in the config, we have defined a default value.

In the last 2 lines we execute our command for each configured file.
As the command routine only registers a new thread and starts it, reusing of this function isn't a problem.

And don't forget to update your ``configuration.py`` file in the application folder::

   CSV_FILES = ["test2.csv"]
   CSV_INTERVAL = 2

From now on our plugin will always watch configured files, even if the command ``csv_watch``
itself is not used by the user.

.. note::
   Do not run ``csv_watch`` on a file, which is also configured to be watched.
   This would result in an exception, as our plugin does not support to monitor a file more than once.

Preparation for documents
-------------------------

Let's create a second plugin, which will show the csv_watcher results inside a document.
Later we will also create some kind of a change history for csv files.

Create a folder ``csv_document_plugin`` inside the plugin folder of your csv_manager package.

Then add two files: ``__init__.py`` and ``csv_document_plugin.py``::

    CSV-Manager
    ├── csv_manager
    │   ├── applications
    │   │   ├── configuration.py
    │   │   ├── csv_manager_app.py
    │   │   └── __init__.py
    │   ├── patterns
    │   │   ├── csv_watcher_pattern
    │   │   │   ├── csv_watcher_pattern.py
    │   │   │   ├── __init__.py
    │   │   │   └── __init__.py
    │   ├── plugins
    │   │   ├── csv_document_plugin
    │   │   │   ├── csv_document_plugin.py
    │   │   │   └── __init__.py
    │   │   ├── csv_watcher_plugin
    │   │   │   ├── csv_watcher_plugin.py
    │   │   │   └── __init__.py
    │   │   ├── csv_manager_plugin.py
    │   │   └── __init__.py
    │   └ ...
    └ ...

Create a document
-----------------

Let's open ``csv_document_plugin.py`` and add the following:

.. code-block:: python
   :linenos:

    from groundwork.patterns import GwDocumentsPattern


    class CsvDocumentPlugin(GwDocumentsPattern):
        def __init__(self, app, **kwargs):
            self.name = self.__class__.__name__
            super().__init__(app, **kwargs)

        def activate(self):
            self.documents.register(name="CsvDocument",
                                    content="CsvDocument Content",
                                    description="Stores pass csv watcher activities")

        def deactivate(self):
            pass

Except line 10, nothing new happened. But as you can see we already have registered a document.

Plugin activation
~~~~~~~~~~~~~~~~~

Before we can see our new document, we have to add our new plugin to the entry_points of our ``setup.py`` file::

    entry_points={
        'console_scripts': ["csv_manager = "
                            "csv_manager.applications.csv_manager_app:start_app"],
        'groundwork.plugin': ["csv_manager_plugin = "
                              "csv_manager.plugins.csv_manager_plugin:"
                              "csv_manager_plugin",  # Do not forget the "," here!
                              "csv_watcher_plugin = "
                              "csv_manager.plugins.csv_watcher_plugin.csv_watcher_plugin:CsvWatcherPlugin",
                              "csv_document_plugin = "
                              "csv_manager.plugins.csv_document_plugin.csv_document_plugin:CsvDocumentPlugin"
                              ],
    }

Then we have to reinstall our csv_manager::

    >>> pip install -e .

And finally we have to add our plugin to the configuration of our application. So open ``config.py`` and
add the following::

    PLUGINS = ["csv_manager_plugin", "GwPluginsInfo", "CsvWatcherPlugin", "CsvDocumentPlugin", "GwDocumentsInfo"]

Attention, we have added 2 plugins: ``CsvDocumentsPlugin`` and ``GwDocumentsInfo``.

``GwDocumentsInfo`` provides the ``doc`` command, which allows us to view documents on the console.

Now we are ready to test it::

    >>> csv_manager doc
    CsvDocument Content
    -------------------------------------------------------------------------------
    This document is registered by 'CsvDocumentPlugin' under the name 'CsvDocument'
    -------------------------------------------------------------------------------
    Actions: [N]ext, E[x]it
    Select your action [N]:

Yeah, that looks great.

Using rst and jinja
-------------------

Right now we do not have really helpful content in our document.
As the content can be huge, we will store it in a new file called ``cvs_document_content.rst`` in our plugin folder.

So let's create it and add the following content:

.. code-block:: jinja
   :linenos:

    CSV Watcher Documentation
    =========================

    Registered csv watchers: ??

groundwork uses `restructured text (rst) <http://docutils.sourceforge.net/rst.html>`_ as syntax.
rst was designed to create human and machine readable text files, which can be transformed to other outputs like
html, pdf, docx, ...

A `brief overview <http://www.sphinx-doc.org/en/1.5.1/rest.html>`_ can be found in the sphinx documentation.

However, you see the two **??** ?. There should be a number, but this number depends on registered watchers. So this
value may change during runtime and can not be hard coded by ourselfs.

Luckily groundwork documents are also supporting `jinja <http://jinja.pocoo.org/docs/2.9/templates/>`_, which is
a template language and allows us to use the content of given python variables.

Change the content to:

.. code-block:: jinja
   :linenos:

    CSV Watcher Documentation
    =========================

    Registered csv watchers: {{ plugin.app.csv_watcher.get()|length}}

In jinja ``{{ VARIABLE/FUNCTION }}`` outputs the data of the given variable or function.
And we use our plugin and its data structure to provide needed data.

As `get()` will deliver a dictionary, we use ``|length`` to get the amount of entries.

.. note::
   Be sure to use ``plugin.app.csv_watcher.get()``! The ``app`` is important otherwise we would
   only get csv_watchers, which were registered by our new plugin. And that's 0.

Ok, this value will still be somehow static, because we do not register new csv_watcher during runtime.

One last thing, we have to mention our new content file during document registration.
So we add it like this in our ``csv_document_plugin.py``:

.. code-block:: python
   :linenos:

   def activate(self):
        this_dir = os.path.dirname(__file__)
        content_path = os.path.join(this_dir, 'csv_document_content.rst')

        with open(content_path, 'r') as doc_content:
            self.documents.register(name="CsvDocument",
                                    content=doc_content.read(),
                                    description="Stores pass csv watcher activities")

There are some challenges to get the correct path for our file:

* We can not use a hard coded path here, because on another system this would be different
* We can also not use a relative path, because it would be relative to the working directory. And this can change.

But we can get the absolute location of the python file, which contains our plugin class.
And we know that our file is stored in the same directory.

Line 2 extracts this directory and line 3 concatenate the folder and the file name. Please do not try to use
string operations for creating a path. In most cases the calculated path would only work on a specific operating system
(e.g. windows uses \\ and linux uses / in paths).

Archive changes
---------------
To change the static behavior let's start to archive the changes from csv_files,
so that we get a living history of changes.

All we need is:

1. Listen to the signal ``csv_watcher_change``.
2. Call a function, which archives the change.
3. Create a archive data object.

So open ``csv_document_plugin.py`` and modify the content to the following:

.. literalinclude:: /../../code/chapter_1/05_documents/CSV-Manager/csv_manager/plugins/csv_document_plugin/csv_document_plugin.py
   :linenos:
   :language: python
   :emphasize-lines: 21-38

The ``_archive_csv_change`` function will add all csv changes to a dictionary.
For each file it will store the current version number (just an integer beginning at 0)
and the related new and missing rows for each version.

This information is also available in a groundwork documents, so let's update our document content file to:

.. code-block:: jinja
   :linenos:

   CSV Watcher Documentation
   =========================

   Registered csv watchers: {{ plugin.app.csv_watcher.get()|length}}

   Files and versions
   ------------------
   {% for key, csv_file in plugin.archive.items() %}
       {{key}}
       {{"~"*key|length}}

       {% for key, version in csv_file["versions"].items() %}
           {{key}}
           Missing: {{version["missing_rows"]}}
           New: {{version["new_rows"]}}
       {% endfor %}
   {% endfor %}


We use some loops here to output our data.

For each csv_file, we write the name and create an underline for it [9-10].
Then for each version inside this csv_file we write the version and after that the missing rows and new rows.

Let's test it and see the output::

   >>> csv_manager doc
   CSV Watcher Documentation
   =========================

   Registered csv watchers: 1

   Files and versions
   ------------------

       test2.csv
       ~~~~~~~~~


           1
           Missing: [{'city': 'London', 'name': 'Paula', 'phone': '1111-222111'}]
           New: [{'city': 'London', 'name': 'Paula', 'phone': '1111-22211'}]

           2
           Missing: [{'city': 'Cologne', 'name': 'Jeanette', 'phone': '111/22223'}]
           New: [{'city': 'Cologne', 'name': 'Julia', 'phone': '111/22223'}]


   -------------------------------------------------------------------------------
   This document is registered by 'CsvDocumentPlugin' under the name 'CsvDocument'
   -------------------------------------------------------------------------------
   Actions: [N]ext, E[x]it
   Select your action [N]:

At the beginning there is no csv_file/version shown on the document page, because no change happened yet.
So for the above output we have changed twice our csv file.

The document must be rendered again, so to perform a "reload" we simply open the next page
and then the previous page again: **n + ENTER; p + ENTER**;

And that's it. You have created a real time documentation of your csv_watcher and you are able
to define files for monitoring in your application configuration.

There is nothing more you could learn about the groundwork framework itself.
But luckily there are still some groundwork extensions: groundwork-database and groundwork-web.

On the next chapter :ref:`chapter_2` we will use a database to store our history
and we take a small look into the database-viewer for web applications.
