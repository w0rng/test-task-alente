from datetime import datetime

from anymail.exceptions import AnymailRequestsAPIError
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = settings.AUTH_USER_MODEL


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


class ForeignUserEvent(models.Model):
    date = models.DateTimeField('Дата создания', default=datetime.now, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    participant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Участник')

    TITLE_MESSAGE = 'Новое событие'
    TEXT_MESSAGE = 'С вашим мероприятием {0} что-то случилось'

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            self.event.author.email_user(self.TITLE_MESSAGE, self.TEXT_MESSAGE.format(self.event.name))
        except AnymailRequestsAPIError:
            pass


class Request(ForeignUserEvent):
    TITLE_MESSAGE = 'Новая заявка'
    TEXT_MESSAGE = 'На ваше мероприятие {0} зарегистрировался новый пользователь'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Feedback(ForeignUserEvent):
    TITLE_MESSAGE = 'Новый отзыв'
    TEXT_MESSAGE = 'Вашему мероприятию {0} оставили новый отзыв'

    file = models.FileField('Дополнительный материал', blank=True, upload_to='feedback')
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        null=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
