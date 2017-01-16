import os
import time
import csv

from groundwork.patterns import GwThreadsPattern
from groundwork.util import gw_get


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
        if self.app.signals.get("csv_watcher_change") is None:
            self.signals.register(signal="csv_watcher_change",
                                  description="indicates a change in a monitored csv file.")


class CsvWatcherPlugin:
    """
    Proxy to the CsvWatcherApplication class.
    Responsible for adding the correct plugin context, if a
    csv_watcher functions gets called inside a plugin
    """

    def __init__(self, plugin):
        self._plugin = plugin
        self._app = plugin.app
        self._watchers = {}

    def register(self, csv_file, interval, description):
        return self._app.csv_watcher.register(csv_file, interval, description, self._plugin)

    def unregister(self, csv_file):
        return self._app.csv_watcher.unregister(csv_file, self._plugin)

    def get(self, csv_file=None):
        return self._app.csv_watcher.get(csv_file, self._plugin)


class CsvWatcherApplication:
    """
    Main class for handling watchers of csv files.
    """

    def __init__(self):
        self._watchers = {}

    def register(self, csv_file, interval, description, plugin):
        if csv_file in self._watchers.keys():
            raise CsvWatcherExistsException("csv file %s is already registered by %s." %
                                            (csv_file, self._watchers[csv_file].plugin.name))

        self._watchers[csv_file] = CsvWatcher(csv_file, interval, description, plugin)
        return self._watchers[csv_file]

    def unregister(self, csv_file, plugin):
        pass

    def get(self, csv_file=None, plugin=None):
        return gw_get(self._watchers, csv_file, plugin)


class CsvWatcher:
    def __init__(self, csv_file, interval, description, plugin):
        self.csv_file = csv_file
        self.interval = interval
        self.plugin = plugin
        self.description = description

        # Register thread
        self.csv_thread = plugin.threads.register("csv_thread_%s" % csv_file, self._csv_watcher_thread,
                                                  "Thread for monitoring a csv file in background")

        self.running = self.csv_thread.running

    def run(self):
        self.csv_thread.run()

    def _csv_watcher_thread(self, plugin):
        csv_file = self.csv_file
        interval = self.interval

        # Check if the given csv_file really exists
        if not os.path.exists(csv_file):
            plugin.log.error("CSV file %s does not exist" % csv_file)

        # Start with an "empty csv file"
        old_content = []

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


class CsvWatcherExistsException(BaseException):
    pass
