import datetime
import logging
import csv
from typing import Dict, Any

from django.contrib.auth import get_user_model
from nameparser import HumanName

from .models import Book, BookAuthor, Author, Binding, Publisher, Reading, Shelf

logger = logging.getLogger('book_manager.importers')

User = get_user_model()


class GoodreadsImporter:
    """
    **Usage**: ``GoodreadsImporter().run(csv_filename, user)``

    Import data into our database from a Goodreeads CSV Export.

    * Import the book from each row as a :py:class:`Book`
    * Import the user specific data from each row as a :py:class:`Reading`
      associated with the user ``user``

    A Goodreads CSV export has these columns:

    +---------------------------------+----------------+------------------------------+
    | Column name                     | Type           | Notes                        |
    +=================================+================+==============================+
    | Book Id                         | int, unique    | goodreads internal id        |
    +---------------------------------+----------------+------------------------------+
    | Title                           | str            |                              |
    +---------------------------------+----------------+------------------------------+
    | Author                          | str            | First Last                   |
    +---------------------------------+----------------+------------------------------+
    | Author l-f                      | str            | Last, First                  |
    +---------------------------------+----------------+------------------------------+
    | Additional Authors              | str            | First Last1, First Last2...  |
    +---------------------------------+----------------+------------------------------+
    | ISBN                            | str            | value is "=" if empty        |
    +---------------------------------+----------------+------------------------------+
    | ISBN13                          | str            | value is "=" if empty        |
    +---------------------------------+----------------+------------------------------+
    | My Rating                       | int            | 0, 1, 2, 3, 4, 5             |
    +---------------------------------+----------------+------------------------------+
    | Average Rating                  | float          | 2 decimals                   |
    +---------------------------------+----------------+------------------------------+
    | Publisher                       | str            | can be empty                 |
    +---------------------------------+----------------+------------------------------+
    | Binding                         | str            | can be empty                 |
    +---------------------------------+----------------+------------------------------+
    | Number of Pages                 | int            | can be empty                 |
    +---------------------------------+----------------+------------------------------+
    | Year Published                  | int            | can be empty                 |
    +---------------------------------+----------------+------------------------------+
    | Original Publication Year       | int            | can be empty                 |
    +---------------------------------+----------------+------------------------------+
    | Date read                       | date           | YYYY/MM/DD                   |
    +---------------------------------+----------------+------------------------------+
    | Date added                      | date           | YYYY/MM/DD                   |
    +---------------------------------+----------------+------------------------------+
    | Bookshelves                     | str            | comma separated              |
    +---------------------------------+----------------+------------------------------+
    | Bookshelves with positions      | str            | NAME (#NUM), comma sep       |
    +---------------------------------+----------------+------------------------------+
    | Exclusive Shelf                 | str            | NAME                         |
    +---------------------------------+----------------+------------------------------+
    | My Review                       | text           | can be empty                 |
    +---------------------------------+----------------+------------------------------+
    | Spoiler                         | text           | can be empty                 |
    +---------------------------------+----------------+------------------------------+
    | Private Notes                   | text           | can be empty                 |
    +---------------------------------+----------------+------------------------------+
    | Read count                      | int            |                              |
    +---------------------------------+----------------+------------------------------+
    | Owned copies                    | int            |                              |
    +---------------------------------+----------------+------------------------------+

    """

    def __init__(self) -> None:
        self.binding_map: Dict[str, Binding] = {}
        self.publisher_map: Dict[str, Publisher] = {}
        self.authors_map: Dict[str, Author] = {}

    def load_lookups(self, filename: str) -> None:
        """
        Find the unique bindings, publishers and authors in the Goodreads export
        CSV ``filename`` and create them in the database as necessary.

        Args:
            filename: the filename of the CSV file to read
        """
        bindings = set()
        publishers = set()
        authors = set()
        with open(filename, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Binding']:
                    bindings.add(row['Binding'])
                if row['Publisher']:
                    publishers.add(row['Publisher'])
                authors.add(row['Author'])
                if row['Additional Authors']:
                    other = row['Additional Authors'].split(', ')
                    authors.update(set(other))

        for binding in list(bindings):
            self.binding_map[binding], created = Binding.objects.get_or_create(name=binding)
            if created:
                logger.info('%s.binding.created name="%s"', self.__class__.__name__, binding)
        for publisher in list(publishers):
            self.publisher_map[publisher], created = Publisher.objects.get_or_create(name=publisher)
            if created:
                logger.info('%s.publisher.created name="%s"', self.__class__.__name__, publisher)
        for name in list(authors):
            n = HumanName(name)
            full_name = str(n)
            author, created = Author.objects.get_or_create(full_name=full_name)
            if created:
                logger.info('%s.author.created full_name="%s"', self.__class__.__name__, full_name)
            author.first_name = n.first
            author.middle_name = n.middle
            author.last_name = n.last
            author.save()
            self.authors_map[full_name] = author

    def import_book(self, row: Dict[str, Any], overwrite: bool = False) -> Book:
        """
        Get or create a :py:class:`Book` based on ``row``, a row from our
        :py:class:`csv.DictReader` reader of our Goodreads export.

        Args:
            row: a row from our Goodreads export

        Keyword Args:
            overwrite: if ``True``, overwrite any existing book data for this book

        Returns:
            A :py:class:`Book` instance
        """
        book, created = Book.objects.get_or_create(title=row['Title'])
        if created or (not created and overwrite):
            isbn = row['ISBN'][1:].strip('"')
            isbn13 = row['ISBN13'][1:].strip('"')
            original_publication_year = row['Original Publication Year']
            if not original_publication_year:
                original_publication_year = None
            book.isbn = isbn if isbn else None
            book.isbn13 = isbn13 if isbn13 else None
            book.num_pages = row['Number of Pages'] if row['Number of Pages'] else None
            book.year_published = row['Year Published'] if row['Year Published'] else None
            book.original_publication_year = original_publication_year
            if row['Binding']:
                book.binding = self.binding_map[row['Binding']]
            if row['Publisher']:
                book.publisher = self.publisher_map[row['Publisher']]
            book.save()
            primary_author = HumanName(row['Author'])
            book.authors.clear()
            author_order = 1
            BookAuthor.objects.create(book=book, author=self.authors_map[str(primary_author)], order=author_order)
            book.authors.add(self.authors_map[str(primary_author)])
            if row['Additional Authors']:
                others = row['Additional Authors'].split(', ')
                for author in others:
                    author_order += 1
                    n = HumanName(author)
                    BookAuthor.objects.create(book=book, author=self.authors_map[str(n)], order=author_order)
        if created:
            logger.info('%s.book.created title="%s"', self.__class__.__name__, book.title)
        else:
            logger.info('%s.book.updated title="%s"', self.__class__.__name__, book.title)
        return book

    def import_reading(self, book: Book, user: User, row: Dict[str, Any]) -> None:
        """
        Import the data for the :py:class:`Reading` record for ``user``.

        Args:
            book: the book for which we're importing reading data
            user: the user whose reading data we're importing
            row: the row from the Goodreads CSV, as output by :py:class:`csv.DictReader`
        """
        shelf, _ = Shelf.objects.get_or_create(reader=user, name=row['Exclusive Shelf'])
        created = False
        try:
            reading = Reading.objects.get(book=book, reader=user)
        except Reading.DoesNotExist:
            created = True
            reading = Reading(book=book, reader=user, shelf=shelf)
        reading.date_added = datetime.datetime.strptime(row['Date Added'], '%Y/%m/%d').date()
        if row['Date Read']:
            reading.date_read = datetime.datetime.strptime(row['Date Read'], '%Y/%m/%d').date()
        if row['Private Notes']:
            reading.private_notes = row['Private Notes']
        if row['My Review']:
            reading.review = row['My Review']
        reading.read_count = row['Read Count'] if row['Read Count'] else 0
        reading.rating = row['My Rating']
        reading.save()
        if created:
            logger.info('%s.reading.created user=%s title="%s"', self.__class__.__name__, user.username, book.title)
        else:
            logger.info('%s.reading.updated user=%s title="%s"', self.__class__.__name__, user.username, book.title)

    def run(self, filename: str, user: User, overwrite: bool = False) -> None:
        """
        Load the books in the CSV identified by ``filename`` into
        the database, splitting each row into appropriate :py:class:`Book`,
        :py:class:`Author`, :py:class:`Publisher` and :py:class:`Binding`
        records, creating the foreign keys and many-to-many targets as
        needed.

        :py:class:`Reading` data will always be overwritten, and
        :py:class:`Book` data will be preserved, unless ``override`` is
        ``True``.

        Args:
            filename: the filename of the Goodreads CSV export file

        Keyword Args:
            overwrite: if ``True``, overwrite any existing :py:class:`Book` with data from the CSV
        """
        self.load_lookups(filename)
        with open(filename, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                book = self.import_book(row, overwrite=overwrite)
                self.import_reading(book, user, row)
