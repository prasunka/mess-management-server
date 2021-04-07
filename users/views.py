from rest_framework import generics
from rest_framework.response import Response

from.models import User
from .serializers import ModeUpdateSerializer

# Create your views here.
class ModeUpdate(generics.UpdateAPIView):
    serializer_class = ModeUpdateSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)