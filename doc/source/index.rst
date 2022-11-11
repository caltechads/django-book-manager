===================
django-book-manager
===================

Current version is |release|.

**Github Repository**: https://github.com/caltechads/django-book-manager

This reusable Django application provides models suitable for managing a list of
books with ratings, somewhat like a private `Goodreads <https://goodreads.com>`_.

Its real purpose is to provide sample models, with sample data, for use in
testing other Django libraries.  Often, when authoring new Django libraries, we
need a simple example application to use so that we can test out our code.

Getting it
==========

You can get ``django-book-manager`` by using pip::

   pip install django-book-manager

If you want to install it from source, grab the git repository from GitHub and run ``setup.py``::

   git clone git://github.com/caltechads/django-book-manager.git
   cd django-book-manager
   python setup.py install

Installing It
=============

To enable ``django-book-manager`` in your project you need to add it to :std:setting:`INSTALLED_APPS`
in your project's ``settings.py`` file::

   INSTALLED_APPS = (
      ...
      'book_manager',
      ...
   )

Then, apply the migrations to add the schema to your database::

   ./manage.py migrate

Using It
========

.. module:: book_manager.models
   :noindex:

Models
------

``django-book-manager`` provides these models:

* :py:class:`Book`:  a book with title, slug, publishing dates, number of pages, authors, etc.
* :py:class:`Author`:  an author.  :py:class:`Book` has a many to many relationship with this
* :py:class:`BookAuthor`:  this is a many to many through table between :py:class:`Book` and :py:class:`Author` that exists to record billing order of authors on a book (first author, second author, etc.)
* :py:class:`Publisher`:  a publisher.  :py:class:`Book` has a foreign key relationship with this
* :py:class:`Binding`: a binding (hardcover, softcover, ebook, ...).  :py:class:`Book` has a foreign key relationship with this

* :py:class:`Reading`: a reading record of a book by a reader.  This is a many to many through table between :py:class:`Book`  and the :std:setting:`AUTH_USER_MODEL` that records a rating, review, notes, date read, etc. for a particular user.
* :py:class:`Shelf`: a collection of :py:class:`Reading` objects, used by readers to classify books

Management commands
-------------------

``django-book-manager`` also supplies a command that can be used to load a
`Goodreads <https://goodreads.com>`_ user library export into Django, splitting
it into all the above models as appropriate.

To generate an export from Goodreads, go to your Goodreads account and:

* Click "My Books"
* At the bottom of that page, click "Import and Export"
* At the top of that page, click "Export Library"

To load the CSV thus generated into Django, first create a user for yourself in Django, then::

   ./manage.py import_csv <csvfile> <username>

A sample Goodreads export is available in this repository as `sandbox/data/books.csv`.


Features:
=========

...

.. toctree::
   :maxdepth: 2

   commands
   api