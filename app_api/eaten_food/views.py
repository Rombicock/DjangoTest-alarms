from django.shortcuts import render
from rest_framework import generics

from eaten_food.models import Meal, EatenFood
from eaten_food.serializers import MealSerializer, EatenFoodSerializer


class MealListAPIView(generics.ListAPIView):
    queryset = Meal.objects.order_by('-date').order_by('-time')
    serializer_class = MealSerializer


class EatenFoodListAPIView(generics.ListAPIView):
    queryset = EatenFood.objects.all()
    serializer_class = EatenFoodSerializer