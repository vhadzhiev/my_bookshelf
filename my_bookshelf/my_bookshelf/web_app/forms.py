from django import forms

from my_bookshelf.web_app.models import Book, Bookshelf

BOOK_ISBN_ERROR_MSG = 'Book with this ISBN already exists for this user'
BOOKSHELF_TITLE_ERROR_MSG = 'Bookshelf with this title already exists for this user'


class CreateBookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            Book.objects.get(isbn=cleaned_data['isbn'], user_id=self.user.id)
        except Book.DoesNotExist:
            pass
        else:
            self.add_error('isbn', BOOK_ISBN_ERROR_MSG)
        return cleaned_data

    class Meta:
        model = Book
        exclude = ('user',)


class CreateBookshelfForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['books'].queryset = Book.objects.all().filter(user_id=self.user.id)

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            Bookshelf.objects.get(title=cleaned_data['title'], user_id=self.user.id)
        except Bookshelf.DoesNotExist:
            pass
        else:
            self.add_error('title', BOOKSHELF_TITLE_ERROR_MSG)
        return cleaned_data

    class Meta:
        model = Bookshelf
        exclude = ('user',)
