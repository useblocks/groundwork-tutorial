import os
from click import Argument, Option
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
        self.csv_interval = None

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
        # Register thread
        csv_thread = self.threads.register("csv_thread", self.csv_watcher_thread,
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

            # Wait x seconds
            time.sleep(plugin.csv_interval)

    def deactivate(self):
        pass
