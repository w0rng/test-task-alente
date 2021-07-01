from django.contrib import admin
from django.db.models import Count

from . import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'start_date', 'author', 'num_participants')

    def num_participants(self, obj):
        return obj.num_participants
    num_participants.short_description = 'Заявок'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(num_participants=Count('request'))


@admin.register(models.Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('participant', 'event', 'date')
