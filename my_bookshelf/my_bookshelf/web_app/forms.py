from django import forms

from my_bookshelf.web_app.models import Book, Bookshelf


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


class CreateBookshelfForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        bookshelf = super().save(commit=False)
        bookshelf.user = self.user
        if commit:
            bookshelf.save()
        return bookshelf

    class Meta:
        model = Bookshelf
        exclude = ('user',)
