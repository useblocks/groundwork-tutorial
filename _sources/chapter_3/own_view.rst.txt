.. _own_view:

Creating own web content
========================

The final chapter is all about creating your first own view with groundwork-web.

Therefore we will create a simple HTML page, which presents the changes of each watcher and has a button to delete the
history of each watcher.

The final result will look like this:

.. image:: /_static/own_web_view.png

Registering route and menu entry
--------------------------------

Open the file ``csv_document_plugin.py`` and perform the following changes:

Add first we need to import some basic flask functions and the need ``GwWebPatter``:

.. literalinclude:: /../../code/chapter_3/01_web/CSV-Manager/csv_manager/plugins/csv_document_plugin/csv_document_plugin.py
   :language: python
   :linenos:
   :lines: 3,7

Then we add this Pattern to our plugin:

.. literalinclude:: /../../code/chapter_3/01_web/CSV-Manager/csv_manager/plugins/csv_document_plugin/csv_document_plugin.py
   :language: python
   :linenos:
   :lines: 13

And finally we add all the magic to ``activate()``:

.. literalinclude:: /../../code/chapter_3/01_web/CSV-Manager/csv_manager/plugins/csv_document_plugin/csv_document_plugin.py
   :language: python
   :linenos:
   :lines: 24-64
   :emphasize-lines: 22-40

In lines 22-27 we register a context, which gets used in line 29 during registration of our view.

Our view shall handle the url ``/history`` and allows the methods ``GET`` and ``POST``.
``POST`` is need for our delte button later.
We also need to add a function/endpoint, which gets executed, if a request to the configured url is incoming.

In lines 34-40 we define a menu entry to make our new web-view easy accessible.

View function
-------------

Now we add the view itself to our plugin:

.. literalinclude:: /../../code/chapter_3/01_web/CSV-Manager/csv_manager/plugins/csv_document_plugin/csv_document_plugin.py
   :language: python
   :linenos:
   :lines: 65-77

Lines 11+12 are the most important ones, because line 11 gets the history data and line 12 renders our HTML page.

The function ``self.web.render`` takes as fist argument the HTML template file name.
After this we can provide as many keyword based arguments as we like. They will be available inside our template.

Lines 3-10 cares about the correct history cleaning, if the button gets pressed.
The code gets executed only, if the request is coming via ``POST`` (Line 3).
After deletion, we want to inform the user that everything got deleted as requests. So we use ``flash()``.



Template
--------

And finally lets create our HTML template file.

Inside the folder of our plugin ``CsvDocumentPlugin``, we create a folder called ``templates``.
And there we add a file ``csv_history.html`` with the following content.

.. literalinclude:: /../../code/chapter_3/01_web/CSV-Manager/csv_manager/plugins/csv_document_plugin/templates/csv_history.html
   :language: html
   :linenos:
   :emphasize-lines: 8

The template uses the `jinja template language <http://jinja.pocoo.org/>`_, which is quite easy to read.

In Line 8 we request the first time our variable ``watchers``, which is available because we have care about this in
the function ``render()`` above.

We uses some for-loops to output our data with {{ .. }}.


Final words
-----------

That's it. Everything is done and running and we are able to see our watchers working.

If you have any questions or ideas, please get in contact with us. The easiest way is by creating an issue on
the github pages of `groundwork-tutorial <https://github.com/useblocks/groundwork-tutorial>`_
or `groundwork <https://github.com/useblocks/groundwork>`_ .





