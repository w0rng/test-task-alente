from datetime import timedelta

from django.utils import timezone

from anymail.exceptions import AnymailRequestsAPIError
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .tasks import subscribe_to_reminder

User = settings.AUTH_USER_MODEL


class Event(models.Model):
    name = models.CharField('Название', max_length=127)
    description = models.TextField('Описание')
    create_date = models.DateTimeField('Дата создания', default=timezone.now, editable=False)
    start_date = models.DateTimeField('Дата проведения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Организатор')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['start_date']
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


class ForeignUserEvent(models.Model):
    date = models.DateTimeField('Дата создания', default=timezone.now, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Участник')

    TITLE_MESSAGE = 'Новое событие'
    TEXT_MESSAGE = 'С вашим мероприятием {0} что-то случилось'

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            self.event.user.email_user(self.TITLE_MESSAGE, self.TEXT_MESSAGE.format(self.event.name))
        except AnymailRequestsAPIError:
            pass


class Request(ForeignUserEvent):
    TITLE_MESSAGE = 'Новая заявка'
    TEXT_MESSAGE = 'На ваше мероприятие {0} зарегистрировался новый пользователь'

    class Meta:
        unique_together = ('event', 'user')
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        subscribe_to_reminder.apply_async(
            (self.user.email, self.event.start_date, self.event.name),
            eta=self.event.start_date - timedelta(days=1)
         )


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
        unique_together = ('event', 'user')
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
