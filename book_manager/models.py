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

    name: F = models.CharField(
        _('Binding type'),
        max_length=128,
        help_text=_('Binding type')
    )

    class Meta:
        verbose_name: str = _('binding')
        verbose_name_plural: str = _('bindings')


class Publisher(TimeStampedModel, models.Model):

    name: F = models.CharField(
        _('Publisher name'),
        max_length=255,
        help_text=_('Publisher name')
    )

    class Meta:
        verbose_name: str = _('publisher')
        verbose_name_plural: str = _('publishers')


class Author(TimeStampedModel, models.Model):

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

    class Meta:
        verbose_name: str = _('author')
        verbose_name_plural: str = _('authors')


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
        related_name='books'
    )
    readers: M2M = models.ManyToManyField(
        get_user_model(),
        verbose_name=_('Owners'),
        related_name='books',
        through='Reading'
    )

    class Meta:
        verbose_name: str = _('book')
        verbose_name_plural: str = _('books')


class Shelf(models.Model):

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

    class Meta:
        verbose_name: str = _('shelf')
        verbose_name_plural: str = _('shelves')


class Reading(TimeStampedModel, models.Model):

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
