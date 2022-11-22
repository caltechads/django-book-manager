.. _api:


Developer Interface
===================

Models
------

.. module:: book_manager.models

This part of the documentation covers all the models provided by ``django-book-manager``.

Books
^^^^^

.. autoclass:: Book
    :members:
    :undoc-members:

.. autoclass:: Author
    :members:
    :undoc-members:

.. autoclass:: BookAuthor
    :members:
    :undoc-members:

.. autoclass:: Publisher
    :members:
    :undoc-members:

.. autoclass:: Binding
    :members:
    :undoc-members:


Readings
^^^^^^^^

A ``Reading`` is a single person's use of a :py:class:`Book`.  It records that
person's notes, ratings, reading count, etc.

.. autoclass:: Reading
    :members:
    :undoc-members:

.. autoclass:: Shelf
    :members:
    :undoc-members:


Widgets
-------

This part of the documentation covers all the reusable `django-wildewidgets
<https://github.com/caltechads/django-wildewidgets>`_ widgets provided by
``django-book-manager``.

.. module:: book_manager.wildewidgets

.. autoclass:: BookManagerMenu
    :members:

.. autoclass:: BookTableWidget
    :members:

.. autoclass:: BookTable
    :members:


Importers
---------

.. module:: book_manager.importers

.. autoclass:: GoodreadsImporter
    :members: