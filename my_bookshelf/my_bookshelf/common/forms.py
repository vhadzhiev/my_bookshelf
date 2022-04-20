from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search by title',
            },
        ),
    )
