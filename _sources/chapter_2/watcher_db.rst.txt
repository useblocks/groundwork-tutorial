.. _watcher_db:

Simple watcher database
=======================

.. note::

   If not done yet, please install **groundwork-database**::

    pip install groundwork-database.


.. sidebar:: Example code

   You can get the complete code of this chapter from
   `github <https://github.com/useblocks/groundwork-tutorial/tree/master/code/chapter_2/01_database/CSV-Manager>`_

During the following steps we will:

* Create a new plugin `CsvWatcherDbPlugin`
* Define some config parameters, which are needed for our database
* Register a SQLite database
* Define and register a database model
* Write functions to add, delete and list watchers




Plugin creation
---------------

At first we need to set up a new plugin. So create a folder `csv_watcher_db_plugin` inside the folder
`csv_manager/plugins`. Then create two files in it: `__init__.py` and `csv_watcher_db_plugin.py`.

Finally let's add some code to our new `csv_watcher_db_plugin.py`::

    from click import Argument, Option

    from groundwork.patterns import GwCommandsPattern
    from groundwork_database.patterns import GwSqlPattern
    from csv_manager.patterns import CsvWatcherPattern


    class CsvWatcherDbPlugin(GwCommandsPattern, CsvWatcherPattern, GwSqlPattern):
        """
        A plugin for monitoring csv files.
        """
        def __init__(self, app, **kwargs):

            self.name = "CsvWatcherDbPlugin"
            super().__init__(app, **kwargs)
            self.db = None

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

        def deactivate(self):
            pass


As you can see, our plugin will provide three new commands to the user: `csv_watcher_list`, `csv_watcher_add` and
`csv_watcher_delete`.

`csv_watcher_list` will provide a list of all stored watchers in our database.
`csv_watcher_add` will add a new watcher to our database, so that it will still be available after an application
restart.
And `csv_watcher_delete` will delete an existing watcher from our database.

But before we can use these functions, we have to setup our database.

Configuration preparation
-------------------------

Currently groundwork-database only supports sql-based database like MySQL, Postgresql, SQLite and more.

We will use `SQLite <https://sqlite.org/>`_,
because it does not need any installation and is
`part of Python's standard library <https://docs.python.org/3.5/library/sqlite3.html>`_.

Let's add the following configurations to our ``configuration.py`` file inside the ``csv_manager/applications`` folder::

    WATCHER_DATABASE_NAME = "WATCHER_DB"
    WATCHER_DATABASE_DESCRIPTION = "DB for CSV file watchers"
    WATCHER_DATABASE_LOCATION = "%s/watcher_db.db" % APP_PATH
    WATCHER_DATABASE_CONNECTION = "sqlite:///%s" % WATCHER_DATABASE_LOCATION


We use the prefix **WATCHER_DATABASE** here to identify easily, which configuration parameters belong to each other.

**NAME** and **DESCRIPTION** is for documentation only. **LOCATION** stores the file path only and becomes
part of the important **CONNECTION** parameter, which contains the database type and the uri, which is used as address
to connect to our database.

.. note::
    Take a look into the
    `SQLAlchemy documentation about Engine Configuration <http://docs.sqlalchemy.org/en/latest/core/engines.html>`_
    for specific information about all supported databases and their needed connection parameter.

Database registration
---------------------

For database registration and configuration we will create a function called ``setup_db()``, which we call in our
``activation()`` routine:

.. code-block:: python
   :linenos:

    def activate(self):
        #  ...
        self.setup_db()


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

groundwork supports the usage and registration of multiple databases. But we only need one, so we register it in
line 7. As return value we get a database object, which we will use for all interactions with our database.

In line 10 we request the SQLAlchemy Base class. SQLAlchemy allows us to define python classes to handle our database
data. But we need to make sure that these classes always inherit from this base class.


Our database table - or better database model - is defined from line 12 to 17.
We use ``__tablename__`` to define our own name for table. If we do not set this value, SQLAlchemy generates a name
based on the class name.

We need and therefore create 3 columns: **id**, **csv_file** and **interval**.

There should be always an id column, so that each row can be clearly identified by this value.
If ``nullable`` is True, the column is allowed to be empty.

Final we register this class on our database [19].

The command ``self.db.create_all()`` tells SQLAlchemy that the configuration is done and that it shall create our
tables, if they do not exist yet.


Working with database models
----------------------------

It's time to use our newly created database model and add some data.

Loading existing watchers
~~~~~~~~~~~~~~~~~~~~~~~~~

But before we can add watchers, we should implement a function, which loads existing watchers and starts
their monitoring thread. So we add a function called ``load_watchers()`` und load it during our ``activate()``
routine:

.. code-block:: python
   :linenos:

    def activate(self):
        #  ...
        self.setup_db()
        load_watchers()

    def load_watchers(self):
        current_watchers = self.Watcher.query.all()
        for watcher in current_watchers:
            try:
                self.activate_watcher(watcher.csv_file, watcher.interval)
            except Exception:
                self.log.error("Couldn't activate watcher for %s" % watcher.csv_file)

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

In line 7 we query for all our watchers from database. All we need for this is our database model class.

As you can see, we can use the return value as a normal python list and iterate over it [8].

And each object in this list is an instance of our database model class, so we are able to access its data like we
would do with other python class [10, 12].

The ``activate_watcher()`` function activates a single watcher. It is not part of the ``load_watchers()`` routine,
because we will reuse it later inside our watcher creation function.

Show watchers
~~~~~~~~~~~~~

Let's add the command function to print a list of currently existing watchers in our database::

    def csv_watcher_list(self):
        watchers = self.Watcher.query.all()
        for watcher in watchers:
            self.log.info("file: %s - interval: %s" % (watcher.csv_file, watcher.interval))

Adding watchers
~~~~~~~~~~~~~~~

And now the interesting part, we create a new watcher:

.. code-block:: python
   :linenos:

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

Before we can create a new watcher, we must be sure that it has not been already added to our database [2-4].

To create a new row in our database table, we need to:

1. Create an instance of our database model and set its values [7]
2. Add this instance to our database [8]
3. And final commit the change to our database [17]

In line 13 we also try to activate our watcher and start the monitoring.

If something goes wrong during creation or activation of our watcher, we are able to rollback all changes [15].


Deleting watchers
~~~~~~~~~~~~~~~~~~

If we can add data, we should also be able to delete data. So lets add the delete function::

    def csv_watcher_delete(self, csv_file):
        self.Watcher.query.filter_by(csv_file=csv_file).delete()
        self.db.commit()
        self.log.info("Watcher for %s removed" % csv_file)

That's it, watchers can now be created and deleted via command line command. And our application does not loose them,
if it gets restarted.

In the next chapter :ref:`history_db` we will use several database models, which have relations to each other.
