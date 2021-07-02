from django.core.mail import send_mail

from core.celery import app


@app.task
def subscribe_to_reminder(email, start_date, name):
    send_mail(
        'Не забудьте про мероприятие',
        f'Завтра ровно в {start_date} начнется мероприятие {name}',
        None, [email]
    )
