from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Event(models.Model):
    name = models.CharField('Название', max_length=127)
    description = models.TextField('Описание')
    create_date = models.DateTimeField('Дата создания', default=datetime.now, editable=False)
    start_date = models.DateTimeField('Дата проведения')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Организатор')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['start_date']
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


class Request(models.Model):
    date = models.DateTimeField('Дата создания', default=datetime.now, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    participant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Участник', related_name='participants')

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
