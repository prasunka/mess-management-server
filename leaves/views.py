from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from .models import Leave
from .serializers import LeaveCreateSerializer, LeaveListSerializer
from .serializers import LeaveUpdateSerializer

# Create your views here.

class LeaveList(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LeaveListSerializer
        else:
            return LeaveCreateSerializer

    def get_queryset(self):
        if self.request.user.typeAccount == 'CATERER':
           return Leave.objects.all()

        return Leave.objects.filter(user=self.request.user.id)

class LeaveUpdate(generics.UpdateAPIView):
    serializer_class = LeaveUpdateSerializer

    def get_queryset(self):
        if self.request.user.typeAccount == 'CATERER':
           return Leave.objects.all()

        return None