from typing import List

from django.urls import path, URLPattern

from .views import (
    ProjectListView
)


app_name: str = "sphinx_hosting"

urlpatterns: List[URLPattern] = [
    path('', ProjectListView.as_view(), name='project--list'),

]
