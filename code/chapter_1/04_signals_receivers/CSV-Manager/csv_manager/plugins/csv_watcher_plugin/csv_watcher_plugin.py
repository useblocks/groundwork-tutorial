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
