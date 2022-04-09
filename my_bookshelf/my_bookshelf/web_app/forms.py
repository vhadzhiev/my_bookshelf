from django import forms

from my_bookshelf.web_app.models import Book


class CreateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('user', )
