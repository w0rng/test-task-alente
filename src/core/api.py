from rest_framework.routers import SimpleRouter
from events import views as event_views

router = SimpleRouter()
router.register('events', event_views.EventViewSet)


__all__ = [
    router,
]
