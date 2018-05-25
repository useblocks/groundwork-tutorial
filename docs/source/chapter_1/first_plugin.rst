.. sidebar:: Content

   .. contents:: ""
      :backlinks: none

.. _first_plugin:

First own plugin
================

In this chapter we will create our first plugin, register a command, work with csv files and create a thread.

But before we start, let's take a look what kind of application and plugins we want to build.


Example Application
-------------------

This tutorial uses one single example application, which gets extend by each chapter.

The overall use case of the example application is the monitoring of changes on comma separated files (CSV files).

CSV files represent a table of information and can be read and saved by office tools like Microsoft Excel, Libreoffice
Calc an others.
They are often used in automation processes and in a lot of cases they are created and updated by scripts.

We want to be able to get notified, if a monitored CSV file gets changed and we also want to know the changes.
In later chapters we will also store these changes in a database, so that we know the history of a CSV file.
And we will also add some kind of a web interface to watch files and history in the browser.

Sequence diagram
~~~~~~~~~~~~~~~~~

The following sequence diagram shows how user, application and plugin interacts with each other and what kind of tasks
must be done during which step.

But don't worry, we will implement these features step by step.

.. uml::
   :scale: 80%

   @startuml
   autonumber

   participant user as u
   participant csv_manager as cm
   participant csv_watcher_plugin as cwp
   participant csv_watcher_plugin.thread as cwpt

   u -> cm : Starts app with\n"csv_watch example.csv"
   cm -> cwp: csv_watcher_plugin.~__init__()
   cm -> cwp: csv_watcher_plugin.activate()
   cwp -> cwp: Register command "csv_watch"
   cm -> cm: starts cli
   cm -> cm: cli checks user command
   cm -> cwp: cli calls csv_watcher_plugin.csv_watcher_command()
   cwp -> cwp: Register new thread "csv_thread"
   cwp -> cwpt: Start thread "csv_thread"
   loop endless
       cwpt -> cwpt: Check given file for changes
           group if changes found
           cwp -> u: Log message "csv file has changed"
           end
       cwpt -> cwpt: Sleep x seconds
   end
   @enduml

Preparation
-----------

Before we can start coding, we have to create a place for our plugin.

Create a folder ``csv_watcher_plugin`` inside the folder ``CSV-Manager/csv_manager/plugins/``.

Inside the newly created folder create two new files: ``__init__.py`` and ``csv_watcher_plugin.py``.

At the end your CSV-Manager should look like this::

   CSV-Manager/
   ├── csv_manager
   │   ├── applications
   │   │   ├── configuration.py
   │   │   ├── csv_manager_app.py
   │   │   └── __init__.py
   │   ├── patterns
   │   │   └── __init__.py
   │   ├── plugins
   │   │   ├── csv_watcher_plugin  # We added this
   │   │   │   ├── csv_watcher_plugin.py  # We added this
   │   │   │   └── __init__.py  # We added this
   │   │   ├── csv_manager_plugin.py
   │   │   └── __init__.py
   │   └─ ...
   └─ ...

.. warning::

   Be sure your ``__init__.py`` is empty and you haven't copy and pasted an ``__init__.py`` file from another location,
   which has some code in it!


Birth of a plugin
-----------------
Now we can start to write our first plugin. Let's start with an empty plugin and add needed functions step by step.

Open ``csv_watcher_plugin.py`` and add the following:

.. code-block:: python
   :linenos:

   from groundwork.patterns import GwBasePattern


   class CsvWatcherPlugin(GwBasePattern):
       """
       A plugin for monitoring csv files.
       """
       def __init__(self, app, **kwargs):
           self.name = "CsvWatcherPlugin"
           super().__init__(app, **kwargs)

       def activate(self):
           pass

       def deactivate(self):
           pass

Each plugin and pattern must inherit from `GwBasePattern`. If you inherit from another pattern, GwBasePattern gets
automatically loaded, because the other pattern already inherits from it [1+4].

There are 4 rules, each plugin must follow:

 1. A name is available in self.name [9]
 2. The __init__() routine of patterns gets called [10]
 3. An activate() routine exists [12]
 4. A deactivate() routine exists [15]

Rule 1,3 and 4 were checked by GwBasePattern during initialisation. If they are not passed, your plugin can not be used.

A missing call of the __init__() routine of patterns (rule 2) may lead to not correct initialised patterns.
For example a database pattern has not initiated its database, because its __init__() routine was not called.

Plugin registration
~~~~~~~~~~~~~~~~~~~
Right now, your plugin exists only in a code file and groundwork does not know it.

But we want be able to load our plugins inside a groundwork app by just adding its name into the related
configuration parameter.

So we have to tell groundwork or better the used Python environment that there is a new plugin.
This can only be done during installation of the CSV-Manager package. And the installation gets its information from
our ``setup.py`` file.

So open ``CSV-Manager/setup.py`` and take a look on the parameter ``entry_points``::

    entry_points={
        'console_scripts': ["csv_manager = "
                            "csv_manager.applications.csv_manager_app:start_app"],
        'groundwork.plugin': ["csv_manager_plugin = "
                              "csv_manager.plugins.csv_manager_plugin:"
                              "csv_manager_plugin"],
    }

``entry_points`` is a python dictionary, which has 2 keys: ``console_scripts`` and ``groundwork.plugin``.

``console_scripts`` are used to register commands for the command line. In this case, it allows us to use
``csv_manager`` as command instead of calling the needed python file with
``python csv_manager/applications/csv_manager_app``.

``groundwork.plugins`` is the place where all the magic happens.
It is a python list and there we need to add our plugin.

An entry of this list is a normal string, which must follow the syntax ``<name> = <packages>:<plugin_class>``.
<name> is not used by groundwork and can be everything.

The needed entry for our plugin is
``csv_watcher_plugin = csv_manager.plugins.csv_watcher_plugin.csv_watcher_plugin:CsvWatcherPlugin``.

Let's add it to our setup.py::

    entry_points={
        'console_scripts': ["csv_manager = "
                            "csv_manager.applications.csv_manager_app:start_app"],
        'groundwork.plugin': ["csv_manager_plugin = "
                              "csv_manager.plugins.csv_manager_plugin:"
                              "csv_manager_plugin",  # Do not forget the "," here!
                              "csv_watcher_plugin = "
                              "csv_manager.plugins.csv_watcher_plugin.csv_watcher_plugin:CsvWatcherPlugin"
                              ],
    }

After saving ``setup.py`` we have to reinstall the ``CSV-Manager``::
   >>> cd CSV-Manager
   >>> pip install -e .

And we also need to add our plugin to the application configuration, so that it gets activated.
Open ``CSV-Manager/csv_manager/applications/configurations.py`` and change the ``PLUGINS = [...]`` line to ::

   PLUGINS = ["csv_manager_plugin", "GwPluginsInfo", "CsvWatcherPlugin"]

First run
~~~~~~~~~

Ok, that's it. Let's see if our plugin really gets activated:

.. code-block:: python
   :linenos:

   >>> csv_manager
   2017-01-14 13:08:14,221 - INFO  - Application signals initialised
   2017-01-14 13:08:14,407 - INFO  - Application commands initialised
   2017-01-14 13:08:14,407 - INFO  - Plugins initialised: csv_manager_plugin
   2017-01-14 13:08:14,408 - INFO  - Application documents initialised
   2017-01-14 13:08:14,408 - INFO  - Plugins initialised: GwPluginsInfo
   2017-01-14 13:08:14,409 - INFO  - Plugins initialised: CsvWatcherPlugin
   2017-01-14 13:08:14,409 - INFO  - Plugins activated: csv_manager_plugin, GwPluginsInfo, CsvWatcherPlugin
   Usage: csv_manager [OPTIONS] COMMAND [ARGS]...

   Options:
     --help  Show this message and exit.

   Commands:
     hello_world  Prints hello world
     plugin_list  List all plugins

Line 7 shows us, that the plugin was found and initiated.
And in line 8 we see that it also got activated.

Using commands
--------------

Now we can start to bring some functionality to our plugin.

At first we should make sure that our functions can be called by the user. For this we need to register a command.

To give our plugin access to command registration, we only need to make sure that our plugin class inherits from
``GwCommandsPattern``:

.. code-block:: python
   :linenos:

    from groundwork.patterns import GwCommandsPattern


    class CsvWatcherPlugin(GwCommandsPattern):
        """
        A plugin for monitoring csv files.
        """
        def __init__(self, app, **kwargs):
            self.name = "CsvWatcherPlugin"
            super().__init__(app, **kwargs)

        def activate(self):
            pass

        def deactivate(self):
            pass

We have changed line 1 and 3 to use ``GwCommandsPattern`` instead of ``GwBasePattern``

The registration of commands should be done inside the ``activation()`` routine to make sure that our commands are only
available, if our plugin really got activated:

.. code-block:: python
   :linenos:

    from groundwork.patterns import GwCommandsPattern


    class CsvWatcherPlugin(GwCommandsPattern):
        """
        A plugin for monitoring csv files.
        """
        def __init__(self, app, **kwargs):
            self.name = "CsvWatcherPlugin"
            super().__init__(app, **kwargs)

        def activate(self):
            self.commands.register("csv_watch",
                                   "Monitors csv files",
                                   self.csv_watcher_command)

        def csv_watcher_command(self):
            self.log.info("watcher command called")

        def deactivate(self):
            pass

And again a test::

    >>> csv_manager
    2017-01-14 15:29:32,742 - INFO  - Application signals initialised
    2017-01-14 15:29:32,956 - INFO  - Application commands initialised
    2017-01-14 15:29:32,957 - INFO  - Plugins initialised: csv_manager_plugin
    2017-01-14 15:29:32,957 - INFO  - Application documents initialised
    2017-01-14 15:29:32,958 - INFO  - Plugins initialised: GwPluginsInfo
    2017-01-14 15:29:32,958 - INFO  - Plugins initialised: CsvWatcherPlugin
    2017-01-14 15:29:32,959 - INFO  - Plugins activated: csv_manager_plugin, GwPluginsInfo, CsvWatcherPlugin
    Usage: csv_manager [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      csv_watch    Monitors csv files  # <--- That's our command.
      hello_world  Prints hello world
      plugin_list  List all plugins

    >>> csv_manager csv_watch
    2017-01-14 15:30:47,952 - INFO  - Application signals initialised
    2017-01-14 15:30:48,134 - INFO  - Application commands initialised
    2017-01-14 15:30:48,135 - INFO  - Plugins initialised: csv_manager_plugin
    2017-01-14 15:30:48,135 - INFO  - Application documents initialised
    2017-01-14 15:30:48,136 - INFO  - Plugins initialised: GwPluginsInfo
    2017-01-14 15:30:48,137 - INFO  - Plugins initialised: CsvWatcherPlugin
    2017-01-14 15:30:48,137 - INFO  - Plugins activated: csv_manager_plugin, GwPluginsInfo, CsvWatcherPlugin
    2017-01-14 15:30:48,137 - INFO  - watcher command called  # <--- That's our output

Adding a command argument
~~~~~~~~~~~~~~~~~~~~~~~~~

Our command gets called, but we still need the information which file our plugin must monitor.
Let's add an argument to our command:

.. code-block:: python
   :linenos:

   from click import  Argument
   from groundwork.patterns import GwCommandsPattern


   class CsvWatcherPlugin(GwCommandsPattern):
       """
       A plugin for monitoring csv files.
       """
       def __init__(self, app, **kwargs):
           self.name = "CsvWatcherPlugin"
           super().__init__(app, **kwargs)

       def activate(self):

           # Argument for our command, which stores the csv file path.
           path_argument = Argument(("csv_file",),
                                    required=True,
                                    type=str)

           self.commands.register("csv_watch",
                                  "Monitors csv files",
                                  self.csv_watcher_command,
                                  params=[path_argument])

       def csv_watcher_command(self, csv_file):
           self.log.info("watcher command called with csv_path: %s" % csv_file)

       def deactivate(self):
           pass

groundwork uses the library `click <http://click.pocoo.org/>`_ for handling the command line interface.
Therefore arguments are defined by using the ``Argument`` class from click [1].

In line 16 - 18 we define our argument. It gets a name and is marked as required. We also define the type, so that we
can be sure that our function always gets a string.

The ``self.commands.register()`` function has a parameters called ``params``, which takes a list of
arguments and options [23].

We have also updated our command function to accept the argument as function parameter [25].
The given csv file location will also be used inside our log message [26].

Time for a small test::

    >>> csv_manager csv_watch test.csv
    2017-01-14 15:51:40,617 - INFO  - Application signals initialised
    2017-01-14 15:51:40,820 - INFO  - Application commands initialised
    2017-01-14 15:51:40,821 - INFO  - Plugins initialised: csv_manager_plugin
    2017-01-14 15:51:40,821 - INFO  - Application documents initialised
    2017-01-14 15:51:40,821 - INFO  - Plugins initialised: GwPluginsInfo
    2017-01-14 15:51:40,822 - INFO  - Plugins initialised: CsvWatcherPlugin
    2017-01-14 15:51:40,823 - INFO  - Plugins activated: csv_manager_plugin, GwPluginsInfo, CsvWatcherPlugin
    2017-01-14 15:51:40,823 - INFO  - watcher command called with csv_path: test.csv  # <-- It works!

Handling csv files
------------------

It's time to start coding the csv handling part of our plugin.
At first we need a way to read the content of a csv file.
Luckily Python provides a built-in solution for this: `The csv module <https://docs.python.org/3/library/csv.html>`_

But before we start, we need a ``test.csv`` file. Create one in the ``CSV-Manager`` folder
and add the following content::

    name,city,phone
    Daniel,Munich,123-456
    Maria,Cologne,111/222
    Richard,Paris,0445-4545-4545
    Anabel,London,-

Now we can write the part for reading the csv file:

.. code-block:: python
   :linenos:

    def csv_watcher_command(self, csv_file):
        self.log.info("watcher command called with csv_path: %s" % csv_file)

        # Check if the given csv_file really exists
        if not os.path.exists(csv_file):
            self.log.error("CSV file %s does not exist" % csv_file)

        with open(csv_file) as csv_file_object:
            reader = csv.DictReader(csv_file_object)
            for row in reader:
                self.log.info(row)

Ok that wasn't much code and all the magic is done in the lines 8-11. As you can see, we read the csv file and
log every single line. Nothing more yet.

And again the test on the command line::

    >>> csv_manager csv_watch test.csv
    2017-01-14 16:32:35,179 - INFO  - Application signals initialised
    2017-01-14 16:32:35,361 - INFO  - Application commands initialised
    2017-01-14 16:32:35,362 - INFO  - Plugins initialised: csv_manager_plugin
    2017-01-14 16:32:35,362 - INFO  - Application documents initialised
    2017-01-14 16:32:35,363 - INFO  - Plugins initialised: GwPluginsInfo
    2017-01-14 16:32:35,364 - INFO  - Plugins initialised: CsvWatcherPlugin
    2017-01-14 16:32:35,364 - INFO  - Plugins activated: csv_manager_plugin, GwPluginsInfo, CsvWatcherPlugin
    2017-01-14 16:32:35,364 - INFO  - watcher command called with csv_path: test.csv
    2017-01-14 16:32:35,365 - INFO  - {'name': 'Daniel', 'city': 'Munich', 'phone': '123-456'}
    2017-01-14 16:32:35,365 - INFO  - {'name': 'Maria', 'city': 'Cologne', 'phone': '111/222'}
    2017-01-14 16:32:35,365 - INFO  - {'name': 'Richard', 'city': 'Paris', 'phone': '0445-4545-4545'}
    2017-01-14 16:32:35,365 - INFO  - {'name': 'Anabel', 'city': 'London', 'phone': '-'}

As you can see, each row is a dictionary and the first row of our csv-file was selected to hold the needed
dictionary key names.

Making csv diffs
~~~~~~~~~~~~~~~~

Our application shall monitor csv files for changes. Therefore it must periodically read a file and compare its
current content with an old, stored content. Let's add this to our ``csv_watcher_command`` function:

.. code-block:: python
   :linenos:

   def csv_watcher_command(self, csv_file):
       self.log.info("watcher command called with csv_path: %s" % csv_file)

       # Check if the given csv_file really exists
       if not os.path.exists(csv_file):
           self.log.error("CSV file %s does not exist" % csv_file)

       # Start with an "empty csv file"
       old_content = []

       while True:
           csv_file_object = open(csv_file)
           new_content = list(csv.DictReader(csv_file_object))

           if new_content != old_content:
               self.log.info("Change detected")

               # Check if there are new/changed rows
               for row in new_content:
                   if row not in old_content:
                       self.log.info("New row: %s" % row)

               # Check if old rows are missing
               for row in old_content:
                   if row not in new_content:
                       self.log.info("Missing row: %s" % row)

               # Store the current csv file content as old content
               old_content = new_content

           csv_file_object.close()

           # Wait 2 seconds
           time.sleep(2)

To allow the easiest way of comparision, the csv content is transformed to a python list, where each list element
represents a single row [13]. After that we compare the old and the new list [15].

The code detects changes per row. If one single value has changed, the whole row is detected as "New row" [19-21].
And the old row is detected as "Missing row" [24-26].

Let's see an output example::

    >>> csv_manager csv_watch test.csv
    2017-01-14 17:20:17,477 - INFO  - Application signals initialised
    2017-01-14 17:20:17,660 - INFO  - Application commands initialised
    2017-01-14 17:20:17,660 - INFO  - Plugins initialised: csv_manager_plugin
    2017-01-14 17:20:17,661 - INFO  - Application documents initialised
    2017-01-14 17:20:17,661 - INFO  - Plugins initialised: GwPluginsInfo
    2017-01-14 17:20:17,662 - INFO  - Plugins initialised: CsvWatcherPlugin
    2017-01-14 17:20:17,662 - INFO  - Plugins activated: csv_manager_plugin, GwPluginsInfo, CsvWatcherPlugin
    2017-01-14 17:20:17,663 - INFO  - watcher command called with csv_path: test.csv
    2017-01-14 17:20:17,663 - INFO  - Change detected
    2017-01-14 17:20:17,663 - INFO  - New row: {'city': 'Munich', 'name': 'Daniel', 'phone': '123-456'}
    2017-01-14 17:20:17,663 - INFO  - New row: {'city': 'Cologne', 'name': 'Maria', 'phone': '111/222'}
    2017-01-14 17:20:17,663 - INFO  - New row: {'city': 'Paris', 'name': 'Richard', 'phone': '0445-4545-4545'}
    2017-01-14 17:20:17,663 - INFO  - New row: {'city': 'London', 'name': 'Anabel', 'phone': '-'}
    2017-01-14 17:20:33,682 - INFO  - Change detected
    2017-01-14 17:20:33,682 - INFO  - New row: {'city': 'London', 'name': 'Anabel', 'phone': '777-888888'}
    2017-01-14 17:20:33,683 - INFO  - Missing row: {'city': 'London', 'name': 'Anabel', 'phone': '-'}
    ^C
    Aborted!

At the beginning the whole csv file content is detected as change, because we compared its content to an empty list.
In :ref:`chapter_2` we will fix this behavior by using a database to store old csv content.

Another problem is that we are using an infinite loop to check our csv-file. See lines 11 and 34 in the code example
above (``while True ...``). Therefore we have to hardly stop our application by pressing **Ctrl + C**.
Also other code from plugins is blocked, too. So in a complex application nothing would work anymore except our
csv watcher code.

Let's fix this by using a thread.

Working with threads
--------------------
Threads can be used on a computer to execute something in parallel to the current execution.
They are an ideal solution for long running tasks like our csv watcher.

groundwork makes the usage of threads very easy. All we need is the ``GwThreadPattern`` and a python function, which
shall be executed in the new thread.

To see the whole picture, here is the complete code of our plugin ``CsvWatcherPlugin``:

.. code-block:: python
   :linenos:

    import os
    from click import  Argument
    import csv
    import time
    from groundwork.patterns import GwCommandsPattern, GwThreadsPattern


    class CsvWatcherPlugin(GwCommandsPattern, GwThreadsPattern):
        """
        A plugin for monitoring csv files.
        """
        def __init__(self, app, **kwargs):
            self.name = "CsvWatcherPlugin"
            super().__init__(app, **kwargs)
            self.csv_file = None

        def activate(self):

            # Argument for our command, which stores the csv file path.
            path_argument = Argument(("csv_file",),
                                     required=True,
                                     type=str)

            self.commands.register("csv_watch",
                                   "Monitors csv files",
                                   self.csv_watcher_command,
                                   params=[path_argument])

        def csv_watcher_command(self, csv_file):
            # Register thread
            self.csv_thread = plugin.threads.register("csv_thread_%s" % csv_file, self._csv_watcher_thread,
                                                      "Thread for monitoring a csv file in background")
            # Start thread
            csv_thread.run()

        def csv_watcher_thread(self, plugin):
            csv_file = plugin.csv_file
            self.log.info("watcher command called with csv_path: %s" % csv_file)

            # Check if the given csv_file really exists
            if not os.path.exists(csv_file):
                self.log.error("CSV file %s does not exist" % csv_file)

            # Start with an "empty csv file"
            old_content = []

            while True:
                csv_file_object = open(csv_file)
                new_content = list(csv.DictReader(csv_file_object))

                if new_content != old_content:
                    self.log.info("Change detected")

                    # Check if there are new/changed rows
                    for row in new_content:
                        if row not in old_content:
                            self.log.info("New row: %s" % row)

                    # Check if old rows are missing
                    for row in old_content:
                        if row not in new_content:
                            self.log.info("Missing row: %s" % row)

                    # Store the current csv file content as old content
                    old_content = new_content

                csv_file_object.close()

                # Wait 2 seconds
                time.sleep(2)

        def deactivate(self):
            pass

We have created a new function ``csv_watcher_thread()`` and moved all code from
``csv_watcher_command()`` to it (see lines 29-72).

``csv_watcher_command()`` is now responsible for registering and starting the thread [32-36].
It also stores the received csv_file to the plugin class itself, so that the thread has access to it [39].

The thread function ``csv_watcher_thread()`` gets a plugin instance as second parameter when the function is called
by the thread-handler. This plugin instance is the instance which has registered the thread.
As our plugin class has done this, the thread function has now access to all plugin variables and functions.
So also to ``csv_file`` [39].

We still have an infinite loop in the thread. Therefore we still must exit our application with **Ctrl + c**.
But compared to the old version, our watcher is not blocking the rest of our application anymore.

Add interval option
-------------------

Currently our application checks the file every 2 seconds. This value is hard coded and that's not a good idea.
We should allow the user to define the interval. So let's change the code a little bit and add an optional command option.

.. code-block:: python
   :linenos:

    from click import Argument, Option

    ...

        def activate(self):

        # Argument for our command, which stores the csv file path.
        path_argument = Argument(("csv_file",),
                                 required=True,
                                 type=str)

        interval_option = Option(("-i", "--interval"),
                                 type=int,
                                 default=10,
                                 help="Sets the time between two checks in seconds")

        self.commands.register("csv_watch",
                               "Monitors csv files",
                               self.csv_watcher_command,
                               params=[path_argument, interval_option])

        def csv_watcher_command(self, csv_file, interval=10):
            ...

        def csv_watcher_thread(self, plugin):
            ...
            # Wait x seconds
            time.sleep(plugin.csv_interval)

Let's check, if the new option is mentioned in the help text for the command::

    >>> csv_manager csv_watch --help
    2017-01-14 18:49:03,390 - INFO  - Application signals initialised
    2017-01-14 18:49:03,595 - INFO  - Application commands initialised
    2017-01-14 18:49:03,595 - INFO  - Plugins initialised: csv_manager_plugin
    2017-01-14 18:49:03,595 - INFO  - Application documents initialised
    2017-01-14 18:49:03,596 - INFO  - Plugins initialised: GwPluginsInfo
    2017-01-14 18:49:03,596 - INFO  - Application threads initialised
    2017-01-14 18:49:03,597 - INFO  - Plugins initialised: CsvWatcherPlugin
    2017-01-14 18:49:03,597 - INFO  - Plugins activated: csv_manager_plugin, GwPluginsInfo, CsvWatcherPlugin
    Usage: csv_manager csv_watch [OPTIONS] CSV_FILE

      Monitors csv files

    Options:
      -i, --interval INTEGER  Sets the time between two checks in seconds
      --help                  Show this message and exit.

That's it, We have created an awesome plugin, which can be started and configured via a command on the command line.

On the next chapter :ref:`first_pattern` we take a look into patterns and make our csv-watcher code reusable for other
plugins.
