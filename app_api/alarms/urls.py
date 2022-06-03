from django.urls import path, include
from .views import AlarmListAPIView, create_alarm, AlarmCRUDApiView, UserListApiView, CustomAuthToken

urlpatterns = [
    path('alarms/', AlarmListAPIView.as_view(), name='all_tasks'),
    path('alarm/create/', create_alarm, name='create_alarm'),
    path('alarm/edit/<int:pk>/', AlarmCRUDApiView.as_view(), name='edit_alarm'),
    path('users/', UserListApiView.as_view()),
    path('auth-token/', CustomAuthToken.as_view())
]