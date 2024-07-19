from django.forms import Form
from .models import Repository


class RepositoryForm(Form):

    class Meta:
        model = Repository
        fields = ['name', 'url', 'issue']
