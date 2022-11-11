from argparse import ArgumentParser

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from book_manager.importers import GoodreadsImporter


User = get_user_model()


class Command(BaseCommand):
    """
    **Usage**: ``./manage.py import_csv [--overwrite] <csvfile> <username>``

    If a book already exists as a :py:class:`Book`, the database entry will not
    be updated unless the `--overwrite` flag is provided.

    `<username>` must refer to an existing Django user.

    See the docstring for :py:class:`GoodreadsImporter` for more information on
    how the import process works.

    """
    args = '[--overwrite] <csvfile> <username>'
    help = ('Imports a Goodreads CSV file into our database.')

    def add_arguments(self, parser: ArgumentParser) -> None:
        """
        :hidden:
        """
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
        """
        :hidden:
        """
        importer = GoodreadsImporter()
        user = User.objects.get(username=options['username'])
        importer.run(options['csvfile'], user, overwrite=options['overwrite'])
