.. sidebar:: Content

   .. contents:: ""
      :backlinks: none


.. _signals_receivers:

Adding signals and receivers
============================

In this chapter we will learn how our pattern can send signals instead of logging text. And how to register
a receiver for this signal inside our plugin.

Signals & receivers are used to provide an easy way of asynchronous communication between plugins.
For instant: one plugin creates a new user and another plugins needs to send a welcome e-mail.

Another advantage is that the sending plugin does not need to know to which plugins it has to send the information.
And the receiving plugins do not need to know, from which plugin they have to collect the information.
Both of them only need to know the signal name.

Register and send signals
-------------------------

Let's add a signal to our ``CsvWatcherPattern`` and remove all log message (or set the log-level to DEBUG):

.. code-block:: python
   :linenos:

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

            # Registers a signal, which get s called every time a change
            # is detected inside an watched csv file.
            if self.signals.get("csv_watcher_change") is None:
                self.signals.register(signal="csv_watcher_change",
                                      description="indicates a change in a monitored csv file.")

        # ... some not changed code ...

        def _csv_watcher_thread(self, plugin):

            # ... some not changed code ...

            while True:
                csv_file_object = open(csv_file)
                new_content = list(csv.DictReader(csv_file_object))

                if new_content != old_content:
                    plugin.log.debug("Change detected")

                    new_rows = []
                    missing_rows = []

                    # Check if there are new/changed rows
                    for row in new_content:
                        if row not in old_content:
                            new_rows.append(row)

                    # Check if old rows are missing
                    for row in old_content:
                        if row not in new_content:
                            missing_rows.append(row)

                    # Store the current csv file content as old content
                    old_content = new_content

                    plugin.signals.send("csv_watcher_change",
                                        csv_file=csv_file,
                                        new_rows=new_rows,
                                        missing_rows=missing_rows)

                csv_file_object.close()

                # Wait x seconds
                time.sleep(interval)

In lines 17-19 we have registered our signals. A signal with the same name can only be registered once.
Therefore we must be sure that we do not register it again, if a second plugin inherits from ``CsvWatcherPattern``.

Instead of logging new or missing rows, we add the changed rows to two lists, which we later send to all
receivers of our signal [40+45].

The final signal is send in line 50. We add two keyword arguments to it: ``new_rows`` and ``missing_rows``.

Register a receiver
-------------------

Right now nothing gets printed, if our pattern detects a change.

Let's change this by adding a receiver to our plugin ``CsvWatcherPlugin`` and
create a function, which logs the changes again. (Changes are highlighted)

.. code-block:: python
   :linenos:
   :emphasize-lines: 34-38, 50-59

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

            self.signals.connect(receiver="csv_change_receiver",
                                 signal="csv_watcher_change",
                                 function=self.csv_change_monitor,
                                 description="Gets called for each csv change")

        def csv_watcher_command(self, csv_file, interval=10):
            self.csv_file = csv_file
            self.csv_interval = interval

            # Register thread
            self.watcher_thread = self.csv_watcher.register(csv_file, interval, "Watcher for %s" % csv_file)

            # Start thread
            self.watcher_thread.run()

        def csv_change_monitor(self, plugin, **kwargs):
            new_rows = kwargs.get("new_rows", None)
            missing_rows = kwargs.get("missing_rows", None)
            csv_file = kwargs.get("csv_file", "unknown file")

            for row in new_rows:
                self.log.info("%s has new row: %s" % (csv_file, row))

            for row in missing_rows:
            self.log.info("%s is missing row: %s" % (csv_file, row))

        def deactivate(self):
            pass

All we need is a function, which shall be called, if the signal is received: ``csv_change_monitor`` [50-59].
And it must be connected to the signal [35-38].

Our function ``csv_change_monitor`` must have 2 parameters: ``plugin`` and ``**kwargs``.

``plugin`` contains the plugin instance, which has connected this function to the signal.
And ``**kwargs`` can contain everything or nothing. It's up by the signal sender to fill data in here.

However, we know that there may be three entries in ``**kwargs``: csv_file, new_rows and missing_rows.
So we try to get them [51-53] and log them [55, 58].

Let it run
----------

Again let's make a test run::

    >>> csv_manager csv_watch -i 5 test.csv
    2017-01-15 15:31:46,425 - INFO  - Application signals initialised
    2017-01-15 15:31:46,624 - INFO  - Application commands initialised
    2017-01-15 15:31:46,624 - INFO  - Plugins initialised: csv_manager_plugin
    2017-01-15 15:31:46,625 - INFO  - Application documents initialised
    2017-01-15 15:31:46,625 - INFO  - Plugins initialised: GwPluginsInfo
    2017-01-15 15:31:46,626 - INFO  - Application threads initialised
    2017-01-15 15:31:46,626 - INFO  - Plugins initialised: CsvWatcherPlugin
    2017-01-15 15:31:46,627 - INFO  - Plugins activated: csv_manager_plugin, GwPluginsInfo, CsvWatcherPlugin
    2017-01-15 15:31:46,627 - INFO  - test.csv has new row: {'phone': '123-4561', 'name': 'Daniel', 'city': 'Munich'}
    2017-01-15 15:31:46,627 - INFO  - test.csv has new row: {'phone': '111/2222', 'name': 'Maria', 'city': 'Cologne'}
    2017-01-15 15:31:46,628 - INFO  - test.csv has new row: {'phone': '0445-4545-45451', 'name': 'Richard', 'city': 'Paris'}
    2017-01-15 15:31:46,628 - INFO  - test.csv has new row: {'phone': '777-8888', 'name': 'Annabel', 'city': 'London'}
    2017-01-15 15:32:11,652 - INFO  - test.csv has new row: {'phone': '1111-222222', 'name': 'Annabel', 'city': 'London'}
    2017-01-15 15:32:11,652 - INFO  - test.csv is missing row: {'phone': '777-8888', 'name': 'Annabel', 'city': 'London'}

Nice, we are now able to add as many plugins to our signal as we like and no unwanted log messages are printed anymore.

On the next chapter :ref:`documents` we will use our new signal to store the changes inside a groundwork document,
which can be used like other groundwork documents for any kind of helpful documentation.
