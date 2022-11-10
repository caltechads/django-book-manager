from argparse import ArgumentParser

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from book_manager.importers import GoodreadsImporter


User = get_user_model()

class Command(BaseCommand):
    """
    Import a Goodreads CSV file into the database.

    A Goodreads export should have these columns:

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
    | My Rating                       | int            |                              |
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
    args = '<csvfile>'
    help = ('Imports a Goodreads CSV file into our database.')

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            'csvfile',
            metavar='csvfile',
            type=str,
            help='The filename of the csvfile to import.'
        )
        parser.add_argument(
            'username',
            metavar='username',
            type=str,
            help='The username of the user whose readings we are importing.'
        )
        parser.add_argument(
            '--overwrite',
            action='store_true',
            default=False,
            help='Overwrite any Book data in the database with data from this file.'
        )

    def handle(self, *args, **options) -> None:
        importer = GoodreadsImporter()
        user = User.objects.get(username=options['username'])
        importer.run(options['csvfile'], user, overwrite=options['overwrite'])
