from django.urls import path
from .views import *

urlpatterns = [
    path('register', UserRegistrationAPIView.as_view(), name='user-register'),
    path('CoordinatorRegistrationAPIView',CoordinatorRegistrationAPIView.as_view(),name='CoordinatorRegistrationAPIView'),

    path('user/<int:user_id>/', UserDetailView.as_view(), name='user-detail'), 
    path('AmbulanceUserListAPIView/',AmbulanceUserListAPIView.as_view(),name='AmbulanceUserListAPIView'),
    path('VolunteerUserAPIView/',VolunteerUserListAPIView.as_view(),name='VolunteerUserListAPIView'),
    path('assign-task/', AssignTaskView.as_view(), name='assign-task'),
    path('assign-taskambulance/', AssignTaskViewAmbulance.as_view(), name='assign-task'),
    path('assign-task/<int:volunteer_id>/', AssignTaskView.as_view(), name='volunteer-tasks'),
    path('LoginPageApi',LoginPageApi.as_view(),name='LoginPageApi'),
    path('incidents/', IncidenttableAPIView.as_view(), name='incident-list'),
    path('volunteerincidents',VolIncidenttableAPIView.as_view(), name='volincident-list'),
    path('incidents/<int:pk>/', IncidenttableDetailAPIView.as_view(), name='incident-detail'),
    path('emergencyalerts/', EmergencyalerttableAPIView.as_view(), name='emergency-list'),
    path('emergencyalerts/<int:pk>/', EmergencyalerttableDetailAPIView.as_view(), name='emergency-detail'),
    path('categories/', CategorytableListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategorytableDetailAPIView.as_view(), name='category-detail'),

    path('resources/', ResourceListCreateAPIView.as_view(), name='resource-list-create'),

    path('viewresourcesallocatedvol/<volunteer_id>',viewresourcesallocatedvol.as_view(),name='viewresourcesallocatedvol'),

    path('donationresources/', DonationResourceListCreateAPIView.as_view(), name='resource-list-create'),

    path('resources/<int:pk>/', ResourceDetailAPIView.as_view(), name='resource-detail'),

    path('amounts/', AmounttableAPIView.as_view(), name='amount-list-create'),
    path('amounts/<int:pk>/', AmounttableAPIView.as_view(), name='amount-detail'),

    path('feedback/', FeedbackListCreateView.as_view(), name='feedback-list-create'),
    path('feedback/<int:pk>/', FeedbackDetailView.as_view(), name='feedback-detail'),

    path('adminListView',adminListView.as_view(),name='adminListView'),

    path('requests/<int:id>/', RequesttableListCreateAPIView.as_view(), name='request-list-create'),
    path('requests/', RequesttableListCreateAPIView.as_view(), name='request-list-create'),
    path('requestsdetail/<int:pk>', RequesttableDetailAPIView.as_view(), name='request-detail'),

    path('requestedresources/<int:pk>', RequesttableDetailAPIView.as_view(), name='requested-detail'),
]



