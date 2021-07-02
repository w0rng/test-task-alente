from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from . import models, serializers, permissions


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
