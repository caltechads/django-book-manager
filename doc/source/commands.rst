Management commands
===================

import_csv
----------

:synposis: Imports a Goodreads CSV export into our database and associate the books listed therein with a Django user.

The ``import_csv`` command imports a Goodreads CSV export into our database,
creating or updating :py:class:`Book` objects (with their dependent
:py:class:`Binding`, :py:class:`Publisher` and :py:class:`Author` objects),
and associates them with user by creating a :py:class:`Reading` object
for each one, and adding the :py:class:`Reading` to a :py:class:`Shelf` as
appropriate.

Why?
^^^^

Goodreads was the model for this package, and its export file matches our
data structure.  It was an easy to get set of rich data.

The export file should have the columns named in the class documentation for
:py:class:`GoodreadsImporter`.

Usage
^^^^^

To generate an export from Goodreads, go to your Goodreads account and:

* Click "My Books"
* At the bottom of that page, click "Import and Export"
* At the top of that page, click "Export Library"

To load that export into the database and associate it with a user with username ``username``::

  $ ./manage.py import_csv goodreads.csv username

To load the export and overwite any existing book data in the database with that in the file::

  $ ./manage.py import_csv --overwrite goodreads.csv username
