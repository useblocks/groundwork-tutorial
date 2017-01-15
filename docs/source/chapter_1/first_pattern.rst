.. sidebar:: Content

   .. contents:: ""
      :backlinks: none


.. _first_pattern:

First own pattern
=================

Patterns are used to provide technical, reusable resources to plugins. They are not related to the content of data,
which they handle. And they provide no final interfaces to the users.
Instead they inject some kind of an API into plugins, which inherit from them.

A pattern gets automatically loaded when the first plugin, which inherit from it, gets initiated and activated.
And it gets deactivated when the last plugin, which inherit from it, gets deactivated.

For our code example this means that the csv watcher would be the perfect pattern.
There are several use cases, where a specific plugin could need the help of a csv watcher pattern.
For instance to monitor measurement results or
to import periodically user data from a provided tool export to another tool.

Preparation
-----------

Before we can start, let's create the needed python packages and files.

Create a folder ``csv_watcher_pattern`` inside the ``patterns`` folder of the csv_manager package.
In the new folder create two additional files: ``__init__.py`` and ``csv_watcher_pattern.py``.::

    >>> tree
    CSV-Manager
    ├── csv_manager
    │   ├── applications
    │   │   ├── configuration.py
    │   │   ├── csv_manager_app.py
    │   │   └── __init__.py
    │   ├── patterns
    │   │   ├── csv_watcher_pattern
    │   │   │   ├── csv_watcher_pattern.py
    │   │   │   └── __init__.py
    │   │   └── __init__.py
    │   └ ...
    └ ...

Code the pattern basement
-------------------------

Open the ``csv_watcher_pattern.py`` file and add the following:

.. code-block:: python
   :linenos:

   from groundwork.patterns import GwThreadsPattern


   class CsvWatcherPattern(GwThreadsPattern):
       def __init__(self, app, **kwargs):
           super().__init__(app, **kwargs)

           # Adds csv_watcher to each plugin
           # This may be done several times. Once for each plugin,
           # which inherits from CsvWatcherPattern
           self.csv_watcher = CsvWatcherPlugin(plugin=self)

           # Adds csv_watcher on application level
           # This is done only once for each application
           if not hasattr(app, "csv_watcher"):
               app.csv_watcher = CsvWatcherApplication()


   class CsvWatcherPlugin:
       """
       Proxy to the CsvWatcherApplication class.
       Responsible for adding the correct plugin context,
       if a csv_watcher functions gets called inside a plugin
       """
       def __init__(self, plugin):
           self._plugin = plugin
           self._app = plugin.app
           self._watchers = {}

       def register(self, csv_file, interval):
           self._app.csv_watcher.register(csv_file, interval, self._plugin)

       def unregister(self, csv_file):
           self._app.csv_watcher.unregister(csv_file, self._plugin)

       def get(self, csv_file=None):
           self._app.csv_watcher.get(csv_file, self._plugin)


   class CsvWatcherApplication:
       """
       Main class for handling watchers of csv files.
       """
       def __init__(self):
           self._watchers = {}

       def register(self, csv_file, interval, plugin):
           pass

       def unregister(self, csv_file, plugin):
           pass

       def get(self, csv_file=None, plugin=None):
           pass

Wow, that's a lot of code for one single step.
But to make our goal clear, we want to be able to register new watchers inside a plugin by using something like
``self.csv_watcher.register()``. We also want to be able to unregister or get watchers, which were registered
by the current plugin only.

Or in others words: A plugin shall only have access to stuff, which it has registered by itself (called plugin context).
That's already the case for groundwork patterns like commands, documents, signals and more.

On the other hand, there must be a way to get access to all watchers. This should be possible by accessing the data
via the application context. Or more detailed: by accessing it via the app object, which is available in each plugin via
``self.app``. In our case we would get all watchers by using ``self.app.csv_watchers.get()``

The above code has already implemented this.
We have one class ``CsvWatcherPlugin`` [19], which cares about functions called in the plugin context.
And another class ``CsvWatcherApplication`` [39], that handles the calls on application level.

To save some code, functions of ``CsvWatcherPlugin`` are mostly calling the related function of
``CsvWatcherApplication``. But they add the current plugin as parameter,
so that the results are filtered for the given plugin.

Example: Lets imagine we are working inside a plugin called "AwesomePlugin" and we register a new watcher via
``self.csv_watcher.register("test.csv")`` [29]. This will call the register function of ``CsvWatcherPlugin``
and inside this function ``app.csv_watcher.register("test.csv", plugin="AwesomePlugin")`` [46] is called, which is part
of ``CsvWatcherApplication``.

The pattern is responsible for creating these contexts and handling the correct initialisation [10-16].

As you can see, we will have 3 new functions inside a plugin which inherits from ``CsvWatcherPattern``:
``register()``, ``unregister`` and ``get()``

``register()`` and ``unregister`` are used to create new watchers or to delete existing ones.
``get()`` provides acccess to existing watchers.

Moving the csv logic
--------------------

Let's move our csv logic from the plugin into our pattern.
We use a new class ``CsvWatcher`` for all functions and information round about a csv watcher.
So it is very easy for a plugin to request a single watcher and get all needed stuff.

.. code-block:: python
   :linenos:

    class CsvWatcher:
        def __init__(self, csv_file, interval, description, plugin):
            self.csv_file = csv_file
            self.interval = interval
            self.plugin = plugin
            self.description = description

            # Register thread
            self.csv_thread = plugin.threads.register("csv_thread", self._csv_watcher_thread,
                                                      "Thread for monitoring a csv file in background")

            self.running = self.csv_thread.running

        def run(self):
            self.csv_thread.run()

        def _csv_watcher_thread(self, plugin):
            csv_file = plugin.csv_file
            interval = plugin.csv_interval
            plugin.log.debug("watcher command called with csv_path: %s and interval: %s" % (csv_file, interval))

            # Check if the given csv_file really exists
            if not os.path.exists(csv_file):
                self.log.error("CSV file %s does not exist" % csv_file)

            # Start with an "empty csv file"
            old_content = []

            while True:
                csv_file_object = open(csv_file)
                new_content = list(csv.DictReader(csv_file_object))

                if new_content != old_content:
                    plugin.log.debug("Change detected")

                    # Check if there are new/changed rows
                    for row in new_content:
                        if row not in old_content:
                            plugin.log.debug("New row: %s" % row)

                    # Check if old rows are missing
                    for row in old_content:
                        if row not in new_content:
                            plugin.log.debug("Missing row: %s" % row)

                    # Store the current csv file content as old content
                    old_content = new_content

                csv_file_object.close()

                # Wait x seconds
                time.sleep(interval)


    class CsvWatcherExistsException(BaseException):
        pass

As you can see, we only have made some minor changes.

We added a ``description`` parameter, so that a plugin can describe the use case during registration of a watcher.

As we are no longer inside a plugin, ``self.log`` will not work. Instead we have to use ``plugin.log`` to create log
messages.

We have also added an exception, which gets called, if the given csv file does not exist.

Now let's take a look into our cleaned plugin class:

.. code-block:: python
   :linenos:

    from click import Argument, Option
    from groundwork.patterns import GwCommandsPattern
    from csv_manager.patterns import CsvWatcherPattern


    class CsvWatcherPlugin(GwCommandsPattern, CsvWatcherPattern):
        """
        A plugin for monitoring csv files.
        """
        def __init__(self, app, **kwargs):

            self.name = "CsvWatcherPlugin"
            super().__init__(app, **kwargs)
            self.csv_file = None
            self.csv_interval = None
            self.watcher_thread = None

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
            self.csv_file = csv_file
            self.csv_interval = interval

            # Register thread
            self.watcher_thread = self.csv_watcher.register(csv_file, interval, "Watcher for %s" % csv_file)

            # Start thread
            self.watcher_thread.run()

        def deactivate(self):
            pass

It has become much short and we have removed some import statements.

Instead of ``GwThreadPattern`` our plugin class inherits from our new ``CsvWatcherPattern`` [6].
Because ``CsvWatcherPattern`` inherits itself from ``GwThreadPattern`` the thread function calls are
still be available in our plugin class (but we do not need them anymore).

Inside the ``csv_watcher_command()`` function we are using our new ``register()`` and ``run()`` functions to handle
our csv watcher [40+43].

All changed files
-----------------
Before we start testing, let's take a look into all changed files.


csv_watcher_pattern.py
~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: /../../code/chapter_1/03_first_pattern/CSV-Manager/csv_manager/patterns/csv_watcher_pattern/csv_watcher_pattern.py
   :language: python
   :linenos:

csv_watcher_plugin.py
~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: /../../code/chapter_1/03_first_pattern/CSV-Manager/csv_manager/plugins/csv_watcher_plugin/csv_watcher_plugin.py
   :language: python
   :linenos:

patterns/__init__.py
~~~~~~~~~~~~~~~~~~~~
We have also imported our pattern inside the __init__.py file of the pattern-package.
With this little change we are able to shorten the import-statement of our pattern to
``from csv_manager.patterns import csv_manager_pattern``.

.. literalinclude:: /../../code/chapter_1/03_first_pattern/CSV-Manager/csv_manager/patterns/__init__.py
   :language: python
   :linenos:

Testing
-------
Let's call our csv_manager and see if it works::

    >>> csv_manager csv_watch -i 5 test.csv
    2017-01-15 10:02:18,232 - INFO  - Application signals initialised
    2017-01-15 10:02:18,417 - INFO  - Application commands initialised
    2017-01-15 10:02:18,418 - INFO  - Plugins initialised: csv_manager_plugin
    2017-01-15 10:02:18,418 - INFO  - Application documents initialised
    2017-01-15 10:02:18,418 - INFO  - Plugins initialised: GwPluginsInfo
    2017-01-15 10:02:18,419 - INFO  - Application threads initialised
    2017-01-15 10:02:18,419 - INFO  - Plugins initialised: CsvWatcherPlugin
    2017-01-15 10:02:18,420 - INFO  - Plugins activated: csv_manager_plugin, GwPluginsInfo, CsvWatcherPlugin
    2017-01-15 10:02:18,420 - INFO  - watcher command called with csv_path: test.csv and interval: 5
    2017-01-15 10:02:18,420 - INFO  - Change detected
    2017-01-15 10:02:18,420 - INFO  - New row: {'city': 'Munich', 'phone': '123-456', 'name': 'Daniel'}
    2017-01-15 10:02:18,420 - INFO  - New row: {'city': 'Cologne', 'phone': '111/222', 'name': 'Maria'}
    2017-01-15 10:02:18,420 - INFO  - New row: {'city': 'Paris', 'phone': '0445-4545-45451', 'name': 'Richard'}
    2017-01-15 10:02:18,421 - INFO  - New row: {'city': 'London', 'phone': '777-888888', 'name': 'Anabel'}

That's it. You have created an awesome pattern, which every plugin can simply use to register watchers for csv files.
And you have updated your plugin to use this pattern.

Sadly there is one ugly problem. Our pattern creates log messages and our plugin gets not informed about changes.

In most cases patterns should not create output to the user. This is the job for the plugin, because only the plugin
is specific enough to really know what kind of information the user needs and how this should be presented
(log, console, website, e-mail, ...).

So in the next chapter :ref:`signals_receivers` we will modify our pattern to send signals instead of writing log
messages. And we create a receiver in our plugin, so that the plugin can present the changes to the user.
