from rest_framework import serializers

from . import models


class EventSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    num_participants = serializers.IntegerField(read_only=True)
    avg_rate = serializers.FloatField(read_only=True, default=0)

    class Meta:
        model = models.Event
        fields = ('name', 'description', 'start_date', 'user', 'num_participants', 'avg_rate')


class RequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Request
        fields = '__all__'
