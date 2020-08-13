from django import forms
from . import models


class SearchForm(forms.Form):
    title = forms.CharField(
        label='タイトル',
        required=False,
        max_length=200
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('name', 'comment')
