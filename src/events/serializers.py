from rest_framework import serializers

from . import models


class EventSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = models.Event
        fields = '__all__'
