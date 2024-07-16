from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View

from .models import Repository


# Create your views here.

class RepositoryView(View):
    model = Repository
    pass
