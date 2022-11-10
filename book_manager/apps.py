from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BookManagerAppConfig(AppConfig):
    name: str = "book_manager"
    label: str = "book_manager"
    verbose_name: str = _("Book Manager")
    default_auto_field: str = "django.db.models.AutoField"
