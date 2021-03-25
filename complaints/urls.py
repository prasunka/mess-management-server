from django.urls import path
from .views import ComplaintList, ComplaintUpdate

urlpatterns = [
    path("", ComplaintList.as_view()),
    path("resolve/<int:pk>/", ComplaintUpdate.as_view()),
]