from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, #Field is optional
                               widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class SearchForm(forms.Form):
    # Not sure below is the best way to be adding classes and attributes to Django Forms...
    query = forms.CharField(widget=forms.TextInput(attrs={'class': "nav-search__input", 'data-target': "searchInput"}))
