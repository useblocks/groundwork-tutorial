#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from _datetime import datetime
from flask import request, flash, url_for

from groundwork.patterns import GwDocumentsPattern
from groundwork_database.patterns import GwSqlPattern
from groundwork_web.patterns import GwWebPattern
from csv_manager.patterns import CsvWatcherPattern

from .models import get_models


class CsvDocumentPlugin(CsvWatcherPattern, GwDocumentsPattern, GwSqlPattern, GwWebPattern):
    def __init__(self, app, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(app, **kwargs)
        self.archive = {}
        self.db = None
        self.CsvFile = None
        self.Version = None
        self.MissingRow = None
        self.NewRow = None

    def activate(self):
        this_dir = os.path.dirname(__file__)
        content_path = os.path.join(this_dir, 'csv_document_content.rst')
        with open(content_path, 'r') as doc_content:
            self.documents.register(name="CsvDocument",
                                    content=doc_content.read(),
                                    description="Stores pass csv watcher activities")

        self.signals.connect("csv_archive_receiver", "csv_watcher_change",
                             self._archive_csv_change, "listen to changes to archive them.")

        self.db = self.databases.register(self.app.config.get("HISTORY_DATABASE_NAME", "csv_history"),
                                          self.app.config.get("HISTORY_DATABASE_CONNECTION", "sqlite://"),
                                          self.app.config.get("HISTORY_DATABASE_DESCRIPTION", "Stores csv history"))
        self.CsvFile, self.Version, self.MissingRow, self.NewRow = get_models(self.db)
        self.db.classes.register(self.CsvFile)
        self.db.classes.register(self.Version)
        self.db.classes.register(self.MissingRow)
        self.db.classes.register(self.NewRow)
        self.db.create_all()

        if self.app.web.contexts.get("csv") is None:
            self.web.contexts.register(name="csv",
                                       template_folder=os.path.join(os.path.dirname(__file__), "templates"),
                                       static_folder=os.path.join(os.path.dirname(__file__), "static"),
                                       url_prefix="/csv",
                                       description="context for csv tasks")

        self.web.routes.register(url="/history",
                                 methods=["GET", "POST"],
                                 endpoint=self._history_view,
                                 context="csv")

        try:
            menu_csv = self.web.menus.register(name="CSV", link="#")
        except Exception:
            menu_csv = self.web.menus.get("CSV")

        with self.app.web.flask.app_context():
            menu_csv.register("History", link=url_for("csv._history_view"))

    def _history_view(self):

        if request.method == 'POST':
            csv_file = request.form['csv_file']
            csv_file_object = self.CsvFile.query.filter_by(name=csv_file).first()
            versions = self.Version.query.filter_by(csv_file=csv_file_object).all()
            for version in versions:
                self.db.session.delete(version)
            self.db.commit()
            flash("Versions of %s deleted" % request.form['csv_file'])
        watchers = self.get_csv_history()
        return self.web.render("csv_history.html", watchers=watchers)

    def _archive_csv_change(self, plugin, **kwargs):
        csv_file = kwargs.get("csv_file", None)
        new_rows = kwargs.get("new_rows", None)
        missing_rows = kwargs.get("missing_rows", None)

        if csv_file is not None:
            # Csc file
            csv_file_object = self.CsvFile.query.filter_by(name=csv_file).first()
            if csv_file_object is None:
                csv_file_object = self.CsvFile(name=csv_file,
                                               created=datetime.now(),
                                               current_version=0)

            csv_file_object.current_version += 1
            self.db.add(csv_file_object)

            # Version
            version_object = self.Version(version=csv_file_object.current_version,
                                          created=datetime.now(),
                                          csv_file=csv_file_object)
            self.db.add(version_object)

            # Missing rows
            for missing_row in missing_rows:
                missing_row_object = self.MissingRow(row=missing_row, version=version_object)
                self.db.add(missing_row_object)

            # New rows
            for new_row in new_rows:
                new_row_object = self.NewRow(row=new_row, version=version_object)
                self.db.add(new_row_object)

            self.db.commit()

            self.log.debug("Change %s archived for %s" % (csv_file_object.current_version, csv_file_object.name))
            self.db.session.remove()

    def get_csv_history(self):
        self.db.session.remove()
        return self.db.query(self.CsvFile).all()

    def deactivate(self):
        pass
