groundwork tutorial
===================

This is the repository of the groundwork tutorial.
It contains the tutorial itself as sphinx project and related example code for each chapter.

**To follow this tutorial, please visit https://useblocks.github.io/groundwork-tutorial/.**

Helpful links
-------------
groundwork
~~~~~~~~~~
| groundwork itself is a plugin-based Python application framework.
| To get a first impression of it, visit http://groundwork.useblocks.com.
| The technical documentation of groundwork can be found at https://groundwork.readthedocs.io

groundwork extensions
~~~~~~~~~~~~~~~~~~~~~

For the technical documentation of **groundwork-database**, visit https://groundwork-database.readthedocs.io.

The documentation for **groundwork-web** can be found at https://groundwork-web.readthedocs.io

Repository structure
--------------------

Directory structure::

    /
    |- code
    |  |- chapter_1  # Example source code for chapter 1: groundwork
    |  |- chapter_2  # Example source code for chapter 2: groundwork-database
    |  |- chapter_3  # Example source code for chapter 3: groundwork-web
    |  |- chapter_n  # Source code of the final example project
    |
    |- docs
       | - source  # Documentation as rst files.


Build docs
----------

To build the documentation, simply do::

    # Get the repository
    git clone https://github.com/useblocks/groundwork-tutorials
    cd groundwork-tutorials/docs

    # Install libraries needed for documentation build
    pip install -r doc-requirements.txt

    # Build documentation
    make html


