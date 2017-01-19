import sys
import os

APP_NAME = "csv_manager_app"
APP_DESCRIPTION = "groundwork application of package CSV-Manager"
APP_PATH = os.path.join(os.path.expanduser('~'), "CSV-Manager")

PLUGINS = ["csv_manager_plugin", "GwPluginsInfo", "CsvWatcherDbPlugin", "CsvDocumentPlugin", "GwDocumentsInfo"]

APP_STRICT = True

CSV_FILES = ["test2.csv"]
CSV_INTERVAL = 2

WATCHER_DATABASE_NAME = "WATCHER_DB"
WATCHER_DATABASE_DESCRIPTION = "DB for CSV file watchers"
WATCHER_DATABASE_LOCATION = "%s/watcher_db.db" % APP_PATH
WATCHER_DATABASE_CONNECTION = "sqlite:///%s" % WATCHER_DATABASE_LOCATION

HISTORY_DATABASE_NAME = "HISTORY_DB"
HISTORY_DATABASE_DESCRIPTION = "DB for CSV history"
HISTORY_DATABASE_LOCATION = "%s/history_db.db" % APP_PATH
HISTORY_DATABASE_CONNECTION = "sqlite:///%s" % HISTORY_DATABASE_LOCATION


GROUNDWORK_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "%(asctime)s - %(levelname)-5s - %(message)s"
        },
        'debug': {
            'format': "%(asctime)s - %(levelname)-5s - %(name)-40s - %(message)-80s - %(module)s:%("
                      "funcName)s(%(lineno)s)"
        },
    },
    'handlers': {
        'console_stdout': {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'level': 'INFO'
        },
        'file': {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "debug",
            "filename": os.path.join(APP_PATH, "csv_manager.log"),
            "maxBytes": 1024000,
            "backupCount": 3,
            'level': 'DEBUG'
        },
        # 'file_my_plugin': {
        #     "class": "logging.handlers.RotatingFileHandler",
        #     "formatter": "debug",
        #     "filename": "logs/my_plugin.log",
        #     "maxBytes": 1024000,
        #     "backupCount": 3,
        #     'level': 'DEBUG'
        # },
    },
    'loggers': {
        '': {
            'handlers': ['console_stdout'],
            'level': 'DEBUG',
            'propagate': False
        },
        'groundwork': {
            'handlers': ['console_stdout', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
        # 'MyPlugin': {
        #     'handlers': ['console_stdout', 'file_my_plugin'],
        #     'level': 'DEBUG',
        #     'propagate': False
        # },
    }
}
