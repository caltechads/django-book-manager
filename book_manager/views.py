from django.views.generic import TemplateView
from wildewidgets import (
    MenuMixin,
    StandardWidgetMixin,
    WidgetListLayout,
)

from .wildewidgets import (
    BookManagerMenu,
    BookManagerBreadcrumbs,
    BookTableWidget,
)


class DashboardView(
    MenuMixin,
    StandardWidgetMixin,
    TemplateView
):
    """
    This is the view we use for the non-user specific home page of the ``book_manager`` app.

    It lists all :py:class:`Book` instances we have in a dataTable.
    """
    template_name = 'academy_theme/base--wildewidgets.html'
    menu_class = BookManagerMenu
    menu_item = "Home"

    def get_content(self):
        layout = WidgetListLayout("Books")
        layout.add_widget(BookTableWidget())
        return layout

    def get_breadcrumbs(self):
        breadcrumbs = BookManagerBreadcrumbs()
        return breadcrumbs
