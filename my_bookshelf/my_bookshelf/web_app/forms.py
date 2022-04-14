from django import forms

from my_bookshelf.web_app.models import Book, Bookshelf


class CreateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('user',)


class CreateBookshelfForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['books'].queryset = Book.objects.all().filter(user_id=self.user.id)

    class Meta:
        model = Bookshelf
        exclude = ('user',)
