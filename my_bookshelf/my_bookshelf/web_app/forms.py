from django import forms

from my_bookshelf.web_app.models import Book


class CreateBookForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        book = super().save(commit=False)
        book.user = self.user
        if commit:
            book.save()
        return book

    class Meta:
        model = Book
        exclude = ('user',)
