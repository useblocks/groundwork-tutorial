.. _history_db:

Complex history database
========================

Databases do not only store data, they are also storing relationships. We will use this feature to
store the change history of our csv files into a database.

This time we will modify our **CsvDocumentPlugin** to store its history data into a database instead of a
dictionary, which would get destroyed with each application exit.

Configuration preparation
-------------------------

Add the following config parameters to the ``configuration.py`` file of your application::

    HISTORY_DATABASE_NAME = "HISTORY_DB"
    HISTORY_DATABASE_DESCRIPTION = "DB for CSV history"
    HISTORY_DATABASE_LOCATION = "%s/history_db.db" % APP_PATH
    HISTORY_DATABASE_CONNECTION = "sqlite:///%s" % HISTORY_DATABASE_LOCATION

Nothing new happened here. We only use a different file for our database.

Model relationships
-------------------

This time we need 4 database model classes. And it's a good idea to store the class definitions
inside a new python file.

So create ``models.py`` in the folder ``csv_manager/plugins/csv_document_plugin`` and add the following content:

.. literalinclude:: /../../code/chapter_2/01_database/CSV-Manager/csv_manager/plugins/csv_document_plugin/models.py
   :language: python
   :linenos:
   :emphasize-lines: 29-30

We put our classes into a function, because we need to provide the db-object [5].
This object will be created during application runtime and therefore it is not available during pythons
instantiation phase.

Let's take a look to the relationship between a csv_file and its versions [29+30].
As you can see, the relationship is defined only on the Version class.

First we a have created a value called **csv_file_id**, which shall store the unique ID of the linked csv_file.
Then we have defined the relationship for the value **csv_file** [30]. If we request this value later, we will
directly get the linked csv_file instance.

But we want also be able to access all linked versions from a csv_file instance, therefore we set the option
**backref**. This options sets a new value into the csv_file, so that all versions can be accessed later via
``csv_file.version``.


The final database model relationship layout is:

.. uml::

   @startuml
   skinparam backgroundColor transparent
   skinparam shadowing false

   class "CsvFile" as cf
   class "Version"  as v
   class "MissingRow" as m
   class "NewRow" as n

   cf <-- v
   v <-- m
   v <-- n

   @enduml


.. note::

   For a deeper look into SQLAlchemy relationships, please visit the related documentation at
   http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html

Storing the history
-------------------

Let's take a look into the final plugin code of your ``csv_document_plugin.py``:

.. literalinclude:: /../../code/chapter_2/01_database/CSV-Manager/csv_manager/plugins/csv_document_plugin/csv_document_plugin.py
   :language: python
   :linenos:
   :emphasize-lines: 33-41, 61-63

Inside the ``activate()`` function you will find the needed database setup and the database model registration [33-41].

The history handling is now completely done inside our database [43-79].

In line 61 you can see an example of how we can set up a relationship between a version and a csv_file.
All we have to do is to use the queried csv_file instance as input for the parameter
**csv_file** of the **Version** class [63].

Retrieving history data
-----------------------

We use our registered document to present stored history data. For this we must be able to retrieve all csv_file objects
from our database inside jinja executions.
For this case we have created the function ``get_csv_history()``, which will be available inside jinja,
because all plugin variables und functions are available inside documents.

Update the file ``csv_document_content.rst`` to get an idea of how it works:

.. literalinclude:: /../../code/chapter_2/01_database/CSV-Manager/csv_manager/plugins/csv_document_plugin/csv_document_content.rst
   :language: jinja
   :linenos:


At that's the end of our groundwork database related chapter.

On the next chapter :ref:`chapter_3` we will use the possibility to create, read, update and delete (CRUD) our database
tables inside a web application with one additional line only. And we will design our own web view to present our just
collected history data inside a browser.









