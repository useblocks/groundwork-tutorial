#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from groundwork.patterns import GwDocumentsPattern
from csv_manager.patterns import CsvWatcherPattern


class CsvDocumentPlugin(CsvWatcherPattern, GwDocumentsPattern):
    def __init__(self, app, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(app, **kwargs)
        self.archive = {}

    def activate(self):
        this_dir = os.path.dirname(__file__)
        content_path = os.path.join(this_dir, 'csv_document_content.rst')
        with open(content_path, 'r') as doc_content:
            self.documents.register(name="CsvDocument",
                                    content=doc_content.read(),
                                    description="Stores pass csv watcher activities")

        self.signals.connect("csv_archive_receiver", "csv_watcher_change",
                             self._archive_csv_change, "listen to changes to archive them.")

    def _archive_csv_change(self, plugin, **kwargs):
        csv_file = kwargs.get("csv_file", None)
        new_rows = kwargs.get("new_rows", None)
        missing_rows = kwargs.get("missing_rows", None)

        if csv_file is not None:
            if csv_file not in self.archive.keys():
                self.archive[csv_file] = {"current_version": 0,
                                          "versions": {}}

            current_version = self.archive[csv_file]["current_version"]
            new_version = current_version + 1
            self.archive[csv_file]["versions"][new_version] = {"new_rows": new_rows,
                                                               "missing_rows": missing_rows}
            self.archive[csv_file]["current_version"] = new_version

    def deactivate(self):
        pass
