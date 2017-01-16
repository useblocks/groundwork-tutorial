import os
from groundwork import App
from csv_manager.applications.configuration import APP_PATH


class CSV_MANAGER_APP:

    def __init__(self):
        # Let's be sure our APP_PATH really exists
        if not os.path.exists(APP_PATH):
            os.makedirs(APP_PATH)
        self.app = App([os.path.join(os.path.dirname(__file__), "configuration.py")])

    def start(self):
        self.app.plugins.activate(self.app.config.get("PLUGINS", None))
        self.app.commands.start_cli()


def start_app():
    CSV_MANAGER_APP().start()


if "main" in __name__:
    start_app()
