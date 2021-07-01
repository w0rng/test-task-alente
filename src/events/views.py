from datetime import datetime

from rest_framework.viewsets import ModelViewSet

from . import models, serializers, permissions


class EventViewSet(ModelViewSet):
    queryset = models.Event.objects.filter(start_date__gt=datetime.now())
    serializer_class = serializers.EventSerializer
    permission_classes = [permissions.IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()
