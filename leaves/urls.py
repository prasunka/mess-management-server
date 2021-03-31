from django.urls import path
from .views import LeaveList, LeaveUpdate

urlpatterns = [
    path("", LeaveList.as_view()),
    path("approve/<int:pk>/", LeaveUpdate.as_view()),
]