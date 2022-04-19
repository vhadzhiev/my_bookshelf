from django import forms
from django.core.exceptions import ValidationError

from my_bookshelf.web_app.models import Book, Bookshelf

BOOK_ISBN_EXCEPTION_MESSAGE = 'You have already added a ook with this ISBN.'
BOOKSHELF_TITLE_EXCEPTION_MESSAGE = 'You have already created a bookshelf with this title.'


class CreateBookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_isbn(self):
        isbn = self.cleaned_data['isbn']
        try:
            Book.objects.get(isbn=isbn, user_id=self.user.id)
        except Book.DoesNotExist:
            pass
        else:
            raise ValidationError(BOOK_ISBN_EXCEPTION_MESSAGE)
        return isbn

    class Meta:
        model = Book
        exclude = ('user',)


class EditBookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.isbn = kwargs.pop('isbn')
        super().__init__(*args, **kwargs)

    def clean_isbn(self):
        isbn = self.isbn
        new_isbn = self.cleaned_data['isbn']

        if isbn != new_isbn:
            try:
                Book.objects.get(isbn=new_isbn, user_id=self.user.id)
            except Book.DoesNotExist:
                pass
            else:
                raise ValidationError(BOOK_ISBN_EXCEPTION_MESSAGE)
        return isbn

    class Meta:
        model = Book
        exclude = ('user',)


class CreateBookshelfForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['books'].queryset = Book.objects.all().filter(user_id=self.user.id).order_by('-date_added')

    def clean_title(self):
        title = self.cleaned_data['title']
        try:
            Bookshelf.objects.get(title=title, user_id=self.user.id)
        except Bookshelf.DoesNotExist:
            pass
        else:
            raise ValidationError(BOOKSHELF_TITLE_EXCEPTION_MESSAGE)
        return title

    class Meta:
        model = Bookshelf
        exclude = ('user',)

    books = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class EditBookshelfForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.title = kwargs.pop('title')
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['books'].queryset = Book.objects.all().filter(user_id=self.user.id).order_by('-date_added')

    def clean_title(self):
        title = self.title
        new_title = self.cleaned_data['title']

        if title != new_title:
            try:
                Bookshelf.objects.get(title=new_title, user_id=self.user.id)
            except Bookshelf.DoesNotExist:
                pass
            else:
                raise ValidationError(BOOKSHELF_TITLE_EXCEPTION_MESSAGE)
        return title

    class Meta:
        model = Bookshelf
        exclude = ('user',)

    books = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

# TODO add placeholders, help text, labels to forms
