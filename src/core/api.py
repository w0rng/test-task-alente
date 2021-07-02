from rest_framework.routers import SimpleRouter
from events import views as event_views

router = SimpleRouter()
router.register('events', event_views.EventViewSet)
router.register('my_events', event_views.MyEventViewSet, basename='my_events')


__all__ = [
    router,
]
