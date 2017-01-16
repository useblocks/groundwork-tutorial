.. _documents:

Using configs and documents
===========================

In this chapter we will learn how to get access on the application configuration,
create a second plugin, which will archive csv changes and show them inside a groundwork document.

Using the config
----------------
Right now our plugin ``CsvWathcerPlugin`` only monitors a file, if the user has requested this by calling the related
command ``csv_watch``.

Let's add the possibility to define a list of file in the configuration, which shall be always monitored.

Open ``csv_watcher_plugin.py`` and add the following code.

Preparation
-----------

Create a folder ``csv_document_plugin`` inside the plugin folder of your csv_manager package.

Then add two files: ``__init__.py`` and ``csv_document_plugin.py``::

    CSV-Manager
    ├── csv_manager
    │   ├── applications
    │   │   │   └── __init__.cpython-35.pyc
    │   │   ├── configuration.py
    │   │   ├── csv_manager_app.py
    │   │   └── __init__.py
    │   ├── patterns
    │   │   ├── csv_watcher_pattern
    │   │   │   │   └── __init__.cpython-35.pyc
    │   │   │   ├── csv_watcher_pattern.py
    │   │   │   ├── __init__.py
    │   │   │   └── __init__.cpython-35.pyc
    │   │   └── __init__.py
    │   ├── plugins
    │   │   ├── csv_document_plugin
    │   │   │   ├── csv_document_plugin.py
    │   │   │   └── __init__.py
    │   │   ├── csv_watcher_plugin  # <--- New
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

Except line 9, nothing new happened. But as you can see we already have registered a document.

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

``GwDocumentsInfo``. provides the ``doc`` command, which allows us to view documents on the console.

Now we are ready to test it::

    >>> csv_manager docs
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

So let's create it and add the following content::

    CSV Watcher Documentation
    =========================

    Registered csv watchers: ??

groundwork uses `restructured text (rst) <http://docutils.sourceforge.net/rst.html>`_ as syntax.
rst was designed to create human and machine readable text files, which can be transformed to other outputs like
html, pdf, docx, ...n

A `brief overview <http://www.sphinx-doc.org/en/1.5.1/rest.html>`_ can be found in the sphinx documentation.

However, you see the two **??** ?. There should be a number, but this numbers depends on registered watchers. So this
value may change during runtime.

Luckily groundwork documents are also supporting `jinja <http://jinja.pocoo.org/docs/2.9/templates/>`_, which is
a template language and allows use to use the content of given python variables.

Change the content to::

    CSV Watcher Documentation
    =========================

    Registered csv watchers: {{ plugin.app.csv_watcher.get()|length}}






1. Second plugin shall perform output and provide a document
2. Create second plugin with just created pattern
3. Add receiver to it. Remove the output from first plugin
4. Register a document
5. Write jinja text
6. Activate plugin
7. Open document viewer
