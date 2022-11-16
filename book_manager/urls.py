from typing import List

from django.urls import path, URLPattern

from .views import (
    DashboardView
)


app_name: str = "book_manager"

urlpatterns: List[URLPattern] = [
    path('', DashboardView.as_view(), name='home'),

]
