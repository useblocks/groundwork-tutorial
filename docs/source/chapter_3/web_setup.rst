.. _web_setup:

Web application setup
=====================

Using GwWeb
-----------

Before we start coding our own views for our new web application, we need to configure our app to support the basic
features for a web application.

Open the file ``configuration.py`` and configure it to use the following plugins::

    PLUGINS = ["csv_manager_plugin", "GwPluginsInfo", "CsvWatcherDbPlugin", "CsvDocumentPlugin", "GwDocumentsInfo",
               "GwWeb", "GwWebManager", ]

As you can see, we have added **GwWeb** and **GwWebManager**.

**GwWeb** will provide command line commands to start a web server. It also handles the configuration and ramp up of
the `flask framework <http://flask.pocoo.org/>`_ in the background.

**GwWebManager** is not really needed, as it *only* provides some views to show groundwork internal data like
registered commands, signals, plugins, web views and much more. It is very helpful for developers to see the current
status of an application without the need of debugging the code for a first overview.


Please also add the following, new configuration parameters to ``configuration.py``::

    FLASK_SERVER_NAME = "127.0.0.1:5000"
    FLASK_HOST = "127.0.0.1"
    FLASK_PORT = 5000
    FLASK_DEBUG = False

These parameters are used to configure `flask <http://flask.pocoo.org/>`_.

**FLASK_SERVER_NAME** must be set to the domain you will use in your browser to view the web application.
This is very important, as flask can handle multiple apps in parallel, which all are registered for different domains
(e.g. example.com and my_site.net). Depending on which domain is called, flask looks into its configuration and
loads the requested view.
So if you use "127.0.0.1:5000" and try to open your site with "localhost:5000", you will get a 404 response for all
views. Please note that also the port must be part of **FLASK_SERVER_NAME**.

**FLASK_HOST** is the external address to which the server gets bound. Normally "127.0.0.1" or "0.0.0.0" are working
well. If your computer provides several outgoing ethernet interfaces, a specific IP may be needed to bound the server to
one interface only.

**FLASK_PORT** stores the port, which shall be used for connections.

And **FLASK_DEBUG** starts the flask server in debugging mode. The debugging mode will catch exceptions and presents
the traceback as web view. It also restarts the server, if it detects changes on related files.
However, it starts the application also twice, in 2 separated processes. Which makes it hard to set breakpoints and
debug it inside an IDE.

Now let's start our new web app and see, if we have configured everything correct by opening the WebManager::

    csv_manager server_start flask_debug

Now open the WebManager at http://127.0.0.1:5000/webmanager/.

That's it. Everything should run now as expected. It's time to take a look into our database via the browser.
Go on with :ref:`db_viewer`.








