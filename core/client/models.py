import datetime

import django.contrib.auth.models
from django.db import models
from django.contrib.auth.models import User
from datetime import time


# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    telegram_id = models.CharField(max_length=50, blank=True, default='')

    def __str__(self):
        return f"Client {self.user.username} id.{self.id}"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class Result(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    objects = models.Manager()
    html_url = models.URLField(max_length=255)
    title = models.CharField(max_length=255, default='Issue')
    labels = models.CharField(max_length=255, default='Labels')
    assignees = models.CharField(max_length=255, default='None')

    def __str__(self):
        return f"Result for {self.client} created at{self.created_at}"
