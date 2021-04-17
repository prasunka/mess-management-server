from django.urls import path
from .views import ModeUpdate

urlpatterns = [
    path("update/mode/<int:pk>/", ModeUpdate.as_view(), name="update_mode"),
]