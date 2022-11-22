from django import forms
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, ButtonHolder, Fieldset, HTML, Div

from book_manager.models import Book, Author


class MinimalBookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'isbn', 'authors']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('title', css_class='border p-3'),
                Field('isbn', css_class='border p-3'),
                Field('authors', css_class='border p-3'),
            ),
            ButtonHolder(
                Div(Submit('submit', 'Add', css_class='btn btn-primary'), css_class='d-flex justify-content-end mt-2'),
            )
        )
