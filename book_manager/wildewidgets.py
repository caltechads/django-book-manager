from typing import List, Tuple, Type, Dict, Any, Optional

from django.templatetags.static import static
from django.urls import reverse
from django.db.models import Model, QuerySet, Count, Q
from wildewidgets import (
    BasicModelTable,
    BreadrumbBlock,
    CardWidget,
    DataTableFilter,
    WidgetListLayoutHeader,
    VerticalDarkMenu
)

from .models import Book, Binding


#------------------------------------------------------
# Navigation
#------------------------------------------------------

class BookManagerMenu(VerticalDarkMenu):
    """
    A main menu for all ``book_manager`` views.   To use it, subclass this and:

    * Add your own menu items it :py:attr:`items`
    * Change the menu logo by updating :py:attr:`brand_image`
    * Change the menu logo alt text by updating :py:attr:`brand_text`
    """

    brand_image: str = static("book_manager/images/logo.jpg")
    brand_image_width: str = "100%"
    brand_text: str = "Book Manager"
    items: List[Tuple[str, str]] = [
        ('Home', 'book_manager:home'),
    ]


class BookManagerBreadcrumbs(BreadrumbBlock):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_breadcrumb('Book Manager', reverse('book_manager:home'))


#------------------------------------------------------
# Template Widgets
#------------------------------------------------------

class BookTableWidget(CardWidget):
    """
    This is a :py:class:`wildewidgets.CardWidget` that gives our Book dataTable a nice
    header with a total book count and an "Add Book" button.
    """
    title: str = "Books"
    icon: str = "window"

    def __init__(self, **kwargs) -> None:
        """
        Regster :py:class:`BookTable` as our "body" content.
        """
        super().__init__(widget=BookTable(), **kwargs)

    def get_title(self) -> WidgetListLayoutHeader:
        header = WidgetListLayoutHeader(
            header_text="Books",
            badge_text=Book.objects.count(),
        )
        header.add_link_button(
            text="New Book",
            color="primary",
            url='#'
        )
        return header


#------------------------------------------------------
# Datatables
#------------------------------------------------------

class BookTable(BasicModelTable):
    """
    This widget displays a `dataTable <https://datatables.net>`_ of our
    :py:class:`Book` instances.

    It's used as a the main widget in by :py:class:`BookTableWidget`.
    """

    model: Type[Model] = Book

    page_length: int = 25  #: Show this many books per page
    striped: bool = True   #: Set to ``True`` to stripe our table rows

    fields: List[str] = [  #: These are the fields on our model (or which are computed) that we will list as columns
        'title',
        'primary_author',
        'other_authors',
        'binding__name',
        'isbn',
        'isbn13',
        'publisher__name',
        'num_pages',
        'original_publication_year',
        'num_readers',
        'created',
        'modified'
    ]
    hidden: List[str] = [  #: These fields will be hidden by default
        'isbn',
        'isbn13',
        'binding__name',
        'created',
        'modified'
    ]
    unsearchable: List[str] = [  #: These columns will not be searched when doing a **global** search
        'num_pages',
        'num_readers',
        'primary_author',
        'other_authors',
    ]
    verbose_names: Dict[str, str] = {  #: Override the default labels labels for the named columns
        'binding__name': 'Binding',
        'primary_author': 'First Author',
        'publisher__name': 'Publisher',
        'original_publication_year': 'Published',
        'num_pages': '# Pages',
        'num_readers': '# Readers'
    }
    alignment: Dict[str, str] = {  #: declare how we horizontally align our columns
        'title': 'left',
        'binding__name': 'left',
        'isbn': 'left',
        'isbn13': 'left',
        'publisher__name': 'left',
        'original_publication_year': 'right',
        'num_pages': 'right',
    }

    def __init__(self, *args, **kwargs) -> None:
        """
        Configure our table filters:

        * Binding name
        * Reader count
        """
        super().__init__(*args, **kwargs)
        binding = DataTableFilter()
        for name in Binding.objects.values_list('name', flat=True):
            binding.add_choice(name, name)
        self.add_filter('binding__name', binding)

        readers = DataTableFilter()
        readers.add_choice('No Readers', 'no_readers')
        readers.add_choice('5 or fewer', 'fewer_than_6')
        readers.add_choice('More than 5', 'more_than_5')
        readers.add_choice('More than 10', 'more_than_10')
        readers.add_choice('More than 20', 'more_than_20')
        self.add_filter('num_readers', readers)

    def search_query(self, qs: "QuerySet[Book]", value: Any) -> Optional[Q]:
        """
        Override :py:meth:`DatatableAJAXView.search_query` so that we also search
        our author names.  Our superclass does not know how to deal with searching
        :py:class:`ManyToManyField` columns.

        Args:
            value: the value for which to search all searchable columns

        Returns:
            A :py:class:`Q` object that ORs ``icontains`` filters for ``value``
            for each searchable column.
        """
        query = super().search_query(qs, value)
        q = Q(authors__full_name__icontains=value)
        query = query | q if query else q
        return query

    def render_other_authors_column(self, row: Book, column: str) -> str:
        """
        Render our ``other_authors`` column as a ``<br>`` separated list of author names.

        Args:
            row: the :py:class:`Book` object we are rendering
            colunn: the name of the column to render

        Returns:
            The list of author names.
        """
        return '<br>'.join(row.other_authors.values_list('full_name', flat=True))

    def render_num_readers_column(self, row: Book, column: str) -> int:
        """
        Render our ``num_readers`` column as the count of :py:class:`Reading`
        instances associated with this :py:class:`Book`.

        Args:
            row: the :py:class:`Book` object we are rendering
            colunn: the name of the column to render

        Returns:
            The number of users who have :py:class:`Reading` associations on
            this book
        """
        return row.readings.all().count()

    def search_num_readers_column(self, qs: "QuerySet[Book]", column: str, value: Any) -> QuerySet:
        """
        Filter our queryset by limiting returned rows to those which have
        ``num_readers`` satisfying ``value`` where ``value`` is a string that
        looks like one of:

        * ``no_readers``: book has 0 readers exactly
        * ``fewers_than_N``: book has fewer than N readers
        * ``more_than_N``: book has more than N readers

        Args:
            qs: a :py:class:`QuerySet` on :py:class:`Book`
            column: the name of the column to filter
            value: the ``num_readers`` filter string

        Raises:
            ValueError: ``value`` is not a valid ``num_readers`` filter string

        Returns:
            Our :py:class:`QuerySet` filtered for according to our ``value``.
        """
        if value == 'no_readers':
            return qs.annotate(reader_count=Count('readers__id')).filter(reader_count=0)
        elif value.startswith('fewer_than_'):
            count = int(value.replace('fewer_than_', ''))
            return qs.annotate(reader_count=Count('readers__id')).filter(reader_count__lt=count)
        elif value.startswith('more_than_'):
            count = int(value.replace('more_than_', ''))
            return qs.annotate(reader_count=Count('readers__id')).filter(reader_count__gt=count)
        else:
            raise ValueError(f'"{value}" is not a known num_readers filter value')

    def search_binding__name_column(self, qs: "QuerySet[Book]", column: str, value: Any) -> QuerySet:
        """
        Filter our queryset by limiting returned rows to those which have a
        binding named ``value``.

        Args:
            qs: a :py:class:`QuerySet` on :py:class:`Book`
            column: the name of the column to filter
            value: the name of the binding

        Returns:
            Our :py:class:`QuerySet` filtered such that only :py:class:`Book`
            instances with bindings with name ``name`` are returned
        """
        return qs.filter(binding__name=value)