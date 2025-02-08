from django.urls import path
from .views import *

urlpatterns = [
    path('register', UserRegistrationAPIView.as_view(), name='user-register'),
    path('user/<int:user_id>/', UserDetailView.as_view(), name='user-detail'), 
    path('AmbulanceUserListAPIView/',AmbulanceUserListAPIView.as_view(),name='AmbulanceUserListAPIView'),
    path('VolunteerUserAPIView/',VolunteerUserListAPIView.as_view(),name='VolunteerUserListAPIView'),
    path('assign-task/', AssignTaskView.as_view(), name='assign-task'),
    path('assign-task/<int:volunteer_id>/', AssignTaskView.as_view(), name='volunteer-tasks'),
    path('LoginPageApi',LoginPageApi.as_view(),name='LoginPageApi'),

]
