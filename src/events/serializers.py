from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from . import models


class EventSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = models.Event
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Request
        fields = '__all__'
