from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Alarm


class AlarmSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Alarm
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = User
        fields = '__all__'