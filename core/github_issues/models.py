from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.

class Repository(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=255)
    issue = models.CharField(max_length=100,
                             choices=settings.ISSUE_CHOICES,
                             default='1')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Repository id.{self.id}, user {self.user} id. {self.user.id}"

    class Meta:
        verbose_name = "Repository"
        verbose_name_plural = "Repositories"
