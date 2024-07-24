from django import forms
from .models import Repository, Label


class RepositoryForm(forms.ModelForm):
    class Meta:
        model = Repository
        fields = ['name', 'url', 'owner']


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name', 'color']
