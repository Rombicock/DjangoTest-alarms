from rest_framework import serializers
from .models import Meal, EatenFood


class MealSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Meal
        fields = '__all__'


class EatenFoodSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = EatenFood
        fields = '__all__'