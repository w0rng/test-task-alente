from django import forms
from . import models
from user.models import User


class EventForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(type=1), label='Автор')

    class Meta:
        model = models.Event
        fields = '__all__'


class RequestForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(type=0), label='Пользователь')

    class Meta:
        model = models.Request
        fields = '__all__'


class FeedbackForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(type=0), label='Пользователь')

    class Meta:
        model = models.Feedback
        fields = '__all__'
