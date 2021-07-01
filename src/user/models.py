from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CHOICES = (
        (0, 'Участник'),
        (1, 'Автор')
    )
    type = models.IntegerField('Тип', choices=CHOICES, default=0)

    def __str__(self):
        return self.get_full_name()
