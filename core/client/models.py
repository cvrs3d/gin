import django.contrib.auth.models
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Client(User):
    telegram_id = models.CharField(max_length=50,
                                   blank=True)

    def __str__(self):
        return f"Client {self.username} id.{self.id}"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
