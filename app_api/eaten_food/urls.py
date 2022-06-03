from django.urls import path, include
from .views import MealListAPIView, EatenFoodListAPIView

urlpatterns = [
    path('meal/', MealListAPIView.as_view(), name='all_tasks'),
    path('eaten_food/', EatenFoodListAPIView.as_view(), name='all_tasks'),
    # path('alarm/create/', create_alarm, name='create_alarm'),
    # path('alarm/edit/<int:pk>/', AlarmCRUDApiView.as_view(), name='edit_alarm'),
]