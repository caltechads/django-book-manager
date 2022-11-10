# django-book-manager

This reusable Django application provides models suitable for managing a list of
books with ratings, somewhat like a private [Goodreads](https://goodreads.com).

Its real purpose is to provide sample models, with sample data, for use in
testing other Django libraries.  Often, when authoring new Django libraries, we
need a simple example application to use so that we can test out our code.

## Getting It

You can get `django-book-manager` by using pip:

```bash
pip install django-book-manager
```

If you want to install it from source, grab the git repository from GitHub and run `setup.py`:

```bash
git clone git://github.com/caltechads/django-book-manager.git
cd django-book-manager
python setup.py install
```

## Installing It

To enable `book_manager` in your project you need to add it to `INSTALLED_APPS`
in your project's `settings.py` file:

```python
INSTALLED_APPS = (
    ...
    'book_manager',
    ...
)
```

Then, apply the migrations to add the schema to your database:

```bash
./manage.py migrate
```

## Using It

`django-book-manager` provides these models:

* `book_manager.Book`:  a book with title, slug, publishing dates, number of pages, authors, etc.
* `book_manager.Author`:  an author.  `book_manager.Book` has a many to many relationship with this
* `book_manager.BookAuthor`:  this is a many to many through table between `book_manager.Book` and `book_manager.Author` that exists to record billing order of authors on a book (first author, second author, etc.)
* `book_manager.Publisher`:  a publisher.  `book_manager.Book` has a foreign key relationship with this
* `book_manager.Binding`: a binding (hardcover, softcover, ebook, ...).  `book_manager.Book` has a foreign key relationship with this

* `book_manager.Reading`: a reading record of a book by a reader.  This is a many to many through table between `book_manager.Book`  and the `AUTH_USER_MODEL` that records a rating, review, notes, date read, etc. for a particular user.
* `book_manager.Shelf`: a collection of `book_manager.Reading` objects, used by readers to classify books

`django-book-manager` also supplies a command that can be used to load a
[Goodreads](https://goodreads.com) user library export into Django, splitting
it into all the above models as appropriate.

To generate an export from Goodreads, go to your Goodreads account and:

* Click "My Books"
* At the bottom of that page, click "Import and Export"
* At the top of that page, click "Export Library"

To load the CSV thus generated into Django, first create a user for yourself in Django, then:

```bash
./manage.py import_csv <csvfile> <username>
```

A sample Goodreads export is available in this repository as `sandbox/data/books.csv`.