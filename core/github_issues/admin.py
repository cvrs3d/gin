from django.contrib import admin
from .models import Repository, Label

# Register your models here.

admin.site.register(Repository)
admin.site.register(Label)
