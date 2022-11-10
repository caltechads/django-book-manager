# Generated by Django 4.1.2 on 2022-11-09 23:37

from django.db import migrations
from django.core.management import call_command

fixture = 'books'


def load_fixture(apps, schema_editor):
    call_command('loaddata', fixture, app_label='core')


def unload_fixture(apps, schema_editor):
    Reading = apps.get_model("book_manager", "Reading")
    Book = apps.get_model("book_manager", "Book")
    Author = apps.get_model("book_manager", "Author")
    Publisher = apps.get_model("book_manager", "Publisher")
    Binding = apps.get_model("book_manager", "Binding")
    Reading.objects.all().delete()
    Book.objects.all().delete()
    Author.objects.all().delete()
    Publisher.objects.all().delete()
    Binding.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('book_manager', '0001_initial'),
        ('users', '0002_load_fixture'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]