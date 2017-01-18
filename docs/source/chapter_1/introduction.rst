.. sidebar:: Content

   .. contents:: ""
      :backlinks: none

Introduction
============

Motivation
----------

What we needed
~~~~~~~~~~~~~~

* Python based plugin system
* use case unbound plugin system
* Combination of code, tests and documentation
* Access to plugin/system meta-data during runtime
* pythonic plugin system
* Plugin activation/deactivation during runtime

What we have found
~~~~~~~~~~~~~~~~~~

* Plugin systems created for use cases: django, flask, qt, pytest ...
* Plugin systems with hard coded constraints (file structure, given names, ...)
* Activation only during application start up

What we have created
~~~~~~~~~~~~~~~~~~~~

A pythonic plugin system, which is designed to be used for each use case and for each tool/library.

Composition
-----------

.. note::
   A more detailed description can be found in the technical documentation of groundwork's
   `architecture <https://groundwork.readthedocs.io/en/latest/architecture.html>`_.

.. uml::

   @startuml

   title "groundwork vs AUTOSAR architecture"

   class "Application\nWeather" as app <<(A, #00aaaa)>>
   class "Plugin\nRegistration" as pa <<(P, #ffcc00)>>
   class "Plugin\nNewsletter" as pb <<(P, #ffcc00)>>
   class "WebPattern" as pta <<(P, #aaaaaa)>>
   class "DatabasePattern" as ptb <<(P, #aaaaaa)>>
   class "EmailPattern" as ptc <<(P, #aaaaaa)>>

   app <-- pa
   app <-- pb

   pa <-- pta
   pa <-- ptb
   pb <-- ptb
   pb <-- ptc

   class "ECU" as ecu <<(A, #00aaaa)>>
   class "SWC A" as sa <<(P, #ffcc00)>>
   class "SWC B" as sb <<(P, #ffcc00)>>
   class "FEM" as fem <<(P, #aaaaaa)>>
   class "RTE" as rte <<(P, #aaaaaa)>>
   class "DEM" as dem <<(P, #aaaaaa)>>

   ecu <-- sa
   ecu <-- sb

   sa <-- fem
   sa <-- rte
   sb <-- rte
   sb <-- dem
   @enduml

Batteries included
------------------

.. note::
   Visit `groundwork.useblocks.com <http://groundwork.useblocks.com>`_ for a nice-looking list of integrated libraries.

* sphinx
* cookiecutter
* click
* blinker
* jinja
* rst
* pytest
* tox
* buildout

Extensions
----------

.. note::
   For a list of known extensions take a look into the
   `related chapter of groundwork's technical documentation <https://groundwork.readthedocs.io/en/latest/packages.html>`_.

* groundwork-web
* groundwork-database


That's enough of the dry theory. Let's start installing something.
Open :ref:`installation`.

