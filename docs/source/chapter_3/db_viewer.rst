.. _db_viewer:

Database views made simple
==========================

Now it's time to use the magic of groundwork patterns to easily extend a plugins functionality.

We will just modify 3-4 lines to get a web view for our database models. This views can then be used to create,
read, update and delete model data in our database.

Web view
--------

We will update our Plugin ``CsvWatcherDbPlugin`` to register views for its models.

So open the file ``csv_watcher_db_plugin.py`` and replace the content with the following code.
Changed lines are highlighted.

.. code-block:: python
   :linenos:
   :emphasize-lines: 3,6,7,11,51,53-59

   from click import Argument, Option
   from sqlalchemy import Column, Integer, String
   from flask import url_for

   from groundwork.patterns import GwCommandsPattern
   # from groundwork_database.patterns import GwSqlPattern #  No longer needed, as GwWebDbAdminPattern inherits from it.
   from groundwork_web.patterns import GwWebDbAdminPattern, GwWebDbRestPattern
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

           try:
               menu_csv = self.web.menus.register(name="CSV", link="#")
           except Exception:
               menu_csv = self.web.menus.get("CSV")
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



As you can see, we haven't made much changes.
We replaced an import and added some new code lines to the ``activation()`` routine.

Instead of ``GwSqlPattern`` we use the ``GwWebDbAdminPattern`` from the groundwork-web package [7].
This pattern inherits itself from ``GwSqlPattern``, so that all functions of this pattern are still available.
So we also changed our class definition to inherit from ``GwWebDbAdminPattern`` [11].

In line 51 we used the functions ``self.web.db.register()`` from ``GwWebDbAdminPattern`` to register our database model **self.Watcher**.
This will automatically activate the views and functions we need to change model data in our browser.

Finally we need a link to the just created view, so that the user must not guess under which url he or she can
edit the model.
So in the lines 53 - 59 we register a menu entry, which will be shown on each page.
Some magic happens in line 59: We use the flask function ``url_for()`` to calculate the correct url for us.
Url links are changing in web applications very often and should never be hard coded somewhere in your code.
``url_for()`` helps us to generate a valid url based on the given view name.

Now restart your server ::

   csv_manager server_start flask_debug

Open the WebManager at http://127.0.0.1:5000/webmanager/.

You should see a new menu entry on the top left of your page. Click it and you will see a table of all csv files,
which were stored inside your database. You are free to use the buttons to create, update or delete some of the data.

.. figure:: /_static/db_web_view.png

   View of the database table of the model **CsvWatchers**


.. note::
   groundwork is using `flask-admin <https://flask-admin.readthedocs.io/en/latest/>`_
   for providing database views.

   Please read the flask-admin documentation for more information how to interact with your new web views.

REST view
---------

Now our users have a nice interface to edit database entries.

But what if an external script needs to make changes to our database and we do not want give direct
database access to it? For this case we can use
`REST <https://en.wikipedia.org/wiki/Representational_state_transfer>`_.

The creation of a REST interface is as easy as the creation of a web interface for a database model.
Just add the following code to the related parts of ``csv_watcher_db_plugin.py``:

.. code-block:: python
   :linenos:

   #  other imports

   from flask_restless import url_for as rest_url_for
   from groundwork_web.patterns import GwWebDbRestPattern

   class CsvWatcherDbPlugin(GwCommandsPattern, CsvWatcherPattern, GwWebDbAdminPattern, GwWebDbRestPattern):

   # ...

   def activate():
   # ...

   self.web.rest.register(self.Watcher, self.db.session)
        with self.app.web.flask.app_context():
            menu_csv.register(name="REST CsvWatchers", link=rest_url_for(self.Watcher))

After a server restart you can see your REST API in action by visiting http://127.0.0.1:5000/api/csv_watchers:

.. figure:: /_static/db_web_rest.png
   :align: center

   REST interface of the database table of the model **CsvWatchers**


.. note::
   groundwork is using `flask-restless <https://flask-restless.readthedocs.io/en/stable/>`_
   for providing REST interfaces.

   Please read the flask-restless documentation for more information how to interact with your new
   REST interface.

Great, you just learned how easy it is to set up views and interfaces to database models. Without any need
to care about HTML, CSS, form validation or any other web related technology.

But luckily we will use these technologies to create our own web view on the next chapter :ref:`own_view`.
