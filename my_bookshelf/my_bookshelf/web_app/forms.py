from django import forms
from django.core.exceptions import ValidationError

from my_bookshelf.web_app.models import Book, Bookshelf

BOOK_ISBN_EXCEPTION_MESSAGE = 'You have already added a book with this ISBN.'
BOOKSHELF_TITLE_EXCEPTION_MESSAGE = 'You have already created a bookshelf with this title.'


class BookCreateForm(forms.ModelForm):
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
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter book\'s title',
                },
            ),
            'author': forms.TextInput(
                attrs={
                    'placeholder': 'Enter book\'s author',
                },
            ),
            'isbn': forms.TextInput(
                attrs={
                    'placeholder': 'Enter book\'s ISBN',
                },
            ),
            'summary': forms.Textarea(
                attrs={
                    'placeholder': 'Enter book\'s summary',
                    'rows': 10,
                },
            ),
        }


class BookEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.isbn = kwargs.pop('isbn')
        super().__init__(*args, **kwargs)

    def clean_isbn(self):
        isbn = self.isbn
        new_isbn = self.cleaned_data['isbn']

        if new_isbn != isbn:
            try:
                Book.objects.get(isbn=new_isbn, user_id=self.user.id)
            except Book.DoesNotExist:
                pass
            else:
                raise ValidationError(BOOK_ISBN_EXCEPTION_MESSAGE)
        return new_isbn

    class Meta:
        model = Book
        exclude = ('user',)
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter book\'s title',
                },
            ),
            'author': forms.TextInput(
                attrs={
                    'placeholder': 'Enter book\'s author',
                },
            ),
            'isbn': forms.TextInput(
                attrs={
                    'placeholder': 'Enter book\'s ISBN',
                },
            ),
            'summary': forms.Textarea(
                attrs={
                    'placeholder': 'Enter book\'s summary',
                    'rows': 10,
                },
            ),
        }


class BookshelfCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['books'].queryset = Book.objects.filter(user_id=self.user.id).order_by('-date_added')

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
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter bookshelf\'s title',
                },
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter bookshelf\'s description',
                    'rows': 5,
                },
            ),
            'books': forms.CheckboxSelectMultiple(),
        }


class BookshelfEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.title = kwargs.pop('title')
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['books'].queryset = Book.objects.filter(user_id=self.user.id).order_by('-date_added')

    def clean_title(self):
        title = self.title
        new_title = self.cleaned_data['title']

        if new_title != title:
            try:
                Bookshelf.objects.get(title=new_title, user_id=self.user.id)
            except Bookshelf.DoesNotExist:
                pass
            else:
                raise ValidationError(BOOKSHELF_TITLE_EXCEPTION_MESSAGE)
        return new_title

    class Meta:
        model = Bookshelf
        exclude = ('user',)
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter bookshelf\'s title',
                },
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter bookshelf\'s description',
                    'rows': 5,
                },
            ),
            'books': forms.CheckboxSelectMultiple(),
        }
