from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from . import models, serializers, permissions, services


class EventViewSet(ModelViewSet):
    queryset = models.Event.objects.filter(start_date__gt=timezone.now())
    serializer_class = serializers.EventSerializer
    permission_classes = [permissions.IsAuthorOrReadOnly, permissions.IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['name']
    search_fields = ['name', 'start_date', 'user__username']
    ordering_fields = ['name', 'start_date', 'user__username']

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


class MyEventViewSet(EventViewSet):
    queryset = None
    permission_classes = [IsAuthenticated, permissions.IsOwnerOrReadOnly]

    def get_queryset(self):
        return services.gey_my_events(self.request.user)


class RequestViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):

    serializer_class = serializers.RequestSerializer
    permission_classes = [IsAuthenticated, permissions.IsParticipant]

    def get_queryset(self):
        return models.Request.objects.filter(user=self.request.user).distinct()

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()
