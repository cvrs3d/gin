from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.

class Repository(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=255)
    objects = models.Manager()
    owner = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repositories')

    def __str__(self):
        return f"Repository id.{self.id}, user {self.user} id. {self.user.id}"

    class Meta:
        verbose_name = "Repository"
        verbose_name_plural = "Repositories"


class Label(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='labels')
    name = models.CharField(max_length=100, default='')
    objects = models.Manager()
    color = models.CharField(max_length=7, default='')

    def __str__(self):
        return self.name


