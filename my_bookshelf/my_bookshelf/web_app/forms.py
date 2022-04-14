from django import forms

from my_bookshelf.web_app.models import Book, Bookshelf


class CreateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('user',)


class CreateBookshelfForm(forms.ModelForm):
    class Meta:
        model = Bookshelf
        exclude = ('user',)
