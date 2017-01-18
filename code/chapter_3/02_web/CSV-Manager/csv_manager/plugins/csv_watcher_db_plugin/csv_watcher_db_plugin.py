from click import Argument, Option
from sqlalchemy import Column, Integer, String
from flask import url_for

from groundwork.patterns import GwCommandsPattern
from groundwork_database.patterns import GwSqlPattern
from groundwork_web.patterns import GwWebDbAdminPattern
from csv_manager.patterns import CsvWatcherPattern


class CsvWatcherDbPlugin(GwCommandsPattern, CsvWatcherPattern, GwWebDbAdminPattern):
    """
    A plugin for monitoring csv files.
    """
    def __init__(self, app, **kwargs):

        self.name = "CsvWatcherDbPlugin"
        super().__init__(app, **kwargs)
        self.db = None
        self.Watcher = None

    def activate(self):

        # Argument for our command, which stores the csv file path.
        path_argument = Argument(("csv_file",),
                                 required=True,
                                 type=str)

        interval_option = Option(("-i", "--interval"),
                                 type=int,
                                 default=10,
                                 help="Sets the time between two checks in seconds")

        self.commands.register("csv_watcher_list",
                               "Shows all csv watchers",
                               self.csv_watcher_list)

        self.commands.register("csv_watcher_add",
                               "Adds a permanent watcher",
                               self.csv_watcher_add,
                               params=[path_argument, interval_option])

        self.commands.register("csv_watcher_delete",
                               "Removes a permanent watcher",
                               self.csv_watcher_delete,
                               params=[path_argument])

        self.setup_db()
        self.load_watchers()

        self.web.db.register(self.Watcher, self.db.session)
        menu_csv = self.web.menus.register(name="CSV", link="#")
        with self.app.web.flask.app_context():
            # Will be http://127.0.0.1:5000/admin/admin_csvwatchers/
            menu_csv.register(name="Watchers", link=url_for("admin_csvwatchers.index_view"))

    def setup_db(self):
        self.db = self.databases.register(self.app.config.get("WATCHER_DATABASE_NAME", "csv_watcher_db"),
                                          self.app.config.get("WATCHER_DATABASE_CONNECTION", "sqlite://"),
                                          self.app.config.get("WATCHER_DATABASE_DESCRIPTION", "Stores csv watchers"))
        Base = self.db.Base

        class CsvWatchers(Base):
            __tablename__ = 'csv_watchers'

            id = Column(Integer, primary_key=True)
            csv_file = Column(String(2048), nullable=False)
            interval = Column(Integer)

        self.Watcher = self.db.classes.register(CsvWatchers)
        self.db.create_all()

    def load_watchers(self):
        current_watchers = self.Watcher.query.all()
        for watcher in current_watchers:
            try:
                self.activate_watcher(watcher.csv_file, watcher.interval)
            except Exception:
                self.log.error("Couldn't activate watcher for %s" % watcher.csv_file)

    def csv_watcher_list(self):
        watchers = self.Watcher.query.all()
        for watcher in watchers:
            self.log.info("file: %s - interval: %s" % (watcher.csv_file, watcher.interval))

    def csv_watcher_add(self, csv_file, interval):
        watcher = self.Watcher.query.filter_by(csv_file=csv_file).first()
        if watcher is not None:
            self.log.error("csv file %s already exists in database." % watcher.csv_file)
        else:
            try:
                watcher = self.Watcher(csv_file=csv_file, interval=interval)
                self.db.add(watcher)
            except Exception:
                self.log.error("Couldn't create csv_file %s in database" % csv_file)
            else:
                try:
                    self.activate_watcher(csv_file, interval)
                except Exception:
                    self.db.rollback()
                else:
                    self.db.commit()

    def csv_watcher_delete(self, csv_file):
        self.Watcher.query.filter_by(csv_file=csv_file).delete()
        self.db.commit()
        self.log.info("Watcher for %s removed" % csv_file)

    def activate_watcher(self, csv_file, interval):
        try:
            # Register thread
            watcher_thread = self.csv_watcher.register(csv_file, interval, "Watcher for %s" % csv_file)

            # Start thread
            if watcher_thread is not None:
                watcher_thread.run()
        except Exception as e:
            raise e
        else:
            self.log.info(("Watcher started for %s" % csv_file))

    def deactivate(self):
        pass
