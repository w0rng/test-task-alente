from django.db.models import QuerySet

from user.models import User
from .models import Event


def gey_my_events(user: User) -> QuerySet[Event]:
    """
    Получает все мероприятия пользователя

    Если это автор, возвращает все мероприятия, которые он создал
    Если это участник, возвращает все мероприятия, на которые он зарегистрирован

    :param user: текущий авторизованный пользователь
    :return: QuerySet всех мероприятий
    """
    if user.type == 0:
        return Event.objects.select_related().filter(request__user=user).distinct()
    elif user.type == 1:
        return Event.objects.filter(user=user)

    return Event.objects.none()
