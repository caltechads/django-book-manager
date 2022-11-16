from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import AutoSlugField

from .validators import NoHTMLValidator


F = models.Field
M2M = models.ManyToManyField
FK = models.ForeignKey


class Binding(models.Model):
    """
    A binding of a :py:class:`Book` ("ebook", "mass market paperback",
    "hardcover", etc.).  Books have zero or one bindings.
    """

    name: F = models.CharField(
        _('Binding type'),
        max_length=128,
        help_text=_('Binding type')
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name: str = _('binding')
        verbose_name_plural: str = _('bindings')


class Publisher(TimeStampedModel, models.Model):
    """
    A publisher of a :py:class:`Book`.  Books have zero or one publishers.
    """

    name: F = models.CharField(
        _('Publisher name'),
        max_length=255,
        help_text=_('Publisher name')
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name: str = _('publisher')
        verbose_name_plural: str = _('publishers')


class Author(TimeStampedModel, models.Model):
    """
    An author of a :py:class:`Book`.  Books can have multiple authors.
    """

    first_name: F = models.CharField(
        _('First name'),
        max_length=255,
    )
    last_name: F = models.CharField(
        _('Last name'),
        max_length=255,
    )
    middle_name: F = models.CharField(
        _('Middle name'),
        max_length=255,
        null=True,
        blank=True,
        default=None
    )
    full_name: F = models.CharField(
        _('Full name'),
        max_length=255,
        unique=True
    )

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name: str = _('author')
        verbose_name_plural: str = _('authors')
        ordering = ['last_name', 'first_name', 'middle_name']


class Book(TimeStampedModel, models.Model):

    title: F = models.CharField(
        _('Book Title'),
        help_text=_('The title of the book'),
        max_length=255,
        unique=True
    )
    slug: F = AutoSlugField(
        _('Slug'),
        unique=True,
        populate_from='title',
        help_text=_('Used in the URL for the book. Must be unique.')
    )
    isbn: F = models.CharField(
        _('ISBN'),
        max_length=16,
        null=True,
        blank=True,
        default=None,
    )
    isbn13: F = models.CharField(
        _('ISBN'),
        max_length=16,
        null=True,
        blank=True,
        default=None,
    )
    num_pages: F = models.PositiveIntegerField(
        _('Num Pages'),
        null=True,
        blank=True,
        default=None,
    )
    year_published: F = models.IntegerField(
        _('Year Published'),
        null=True,
        blank=True,
        default=None,
    )
    original_publication_year: F = models.IntegerField(
        _('Original Publication Year'),
        null=True,
        blank=True,
        default=None,
    )
    binding: FK = models.ForeignKey(
        Binding,
        on_delete=models.SET_NULL,
        related_name='books',
        null=True
    )
    publisher: FK = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='books',
        null=True
    )
    authors: M2M = models.ManyToManyField(
        Author,
        verbose_name=_('Authors'),
        related_name='books',
        through='BookAuthor'
    )
    readers: M2M = models.ManyToManyField(
        get_user_model(),
        verbose_name=_('Readers'),
        related_name='books',
        through='Reading'
    )

    @property
    def primary_author(self) -> Author:
        """
        Return the top-billed author for this book.  This is the author
        with ``order=1`` in our :py:class:`BookAuthor` through table.

        Returns:
            The :py:class:`Author` object for the primary author
        """
        return self.authors.get(bookauthor__order=1)

    @property
    def other_authors(self) -> "models.QuerySet[Author]":
        """
        Return all authors other than the top-billed author for this book.
        These are the authors with ``order>1`` in our :py:class:`BookAuthor`
        through table.

        Returns:
            The queryset of :py:class:`Author` objects for the non-primary
            author.
        """
        return self.authors.filter(bookauthor__order__gt=1)

    class Meta:
        verbose_name: str = _('book')
        verbose_name_plural: str = _('books')
        ordering = ['title']


class BookAuthor(models.Model):
    """
    This is a through table between :py:class:`Book` and :py:class:`Author` that
    allows us to keep our book authors in the correct order.
    """

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name=_('Author'),
    )
    order = models.PositiveIntegerField(
        _('Author order'),
        default=1
    )

    class Meta:
        unique_together = ('book', 'author', 'order')
        verbose_name: str = _('book author')
        verbose_name_plural: str = _('book authors')
        ordering = ('book', 'order',)


class Shelf(models.Model):
    """
    This model is used to organize :py:class:`Reading` instances for a user into
    buckets ("read", "to-read", "abandoned").  Shelves are per-user.
    """

    name: F = models.CharField(
        _('Shelf name'),
        max_length=128,
        help_text=_('Name of a shelf on which books can live')
    )

    reader = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_('Reader'),
        related_name='shelves'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name: str = _('shelf')
        verbose_name_plural: str = _('shelves')


class Reading(TimeStampedModel, models.Model):
    """
    This model holds user-specific data about a reading of a :py:class:`Book`
    """

    rating = models.PositiveIntegerField(
        _('Rating'),
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
    private_notes = models.TextField(
        _('Private Notes'),
        help_text=_('Private notes that only you can see'),
        blank=True,
        null=True,
        default=None,
        validators=[NoHTMLValidator()]
    )
    review = models.TextField(
        _('Review'),
        help_text=_('Notes that anyone can see'),
        blank=True,
        null=True,
        default=None,
        validators=[NoHTMLValidator()]
    )
    read_count = models.PositiveIntegerField(
        _('Read count'),
        help_text=_("How many times you've read this book")
    )
    date_added = models.DateField(
        _('Date added'),
        help_text=_("Date this book was added to your reading list")
    )
    date_read = models.DateField(
        _('Date read'),
        help_text=_("Date you first read this book"),
        null=True,
        default=None
    )

    reader = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_('Reader'),
        related_name='readings'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='readings'
    )
    shelf = models.ForeignKey(
        Shelf,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name='readings'
    )

    class Meta:
        verbose_name: str = _('reading')
        verbose_name_plural: str = _('readings')
