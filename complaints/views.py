from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from .models import Complaint
from .serializers import ComplaintListSerializer, ComplaintCreateSerializer
from .serializers import ComplaintUpdateSerializer
# Create your views here.


class ComplaintList(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ComplaintListSerializer
        else:
            return ComplaintCreateSerializer

    def get_queryset(self):
        return Complaint.objects.filter(user=self.request.user.id)

class ComplaintUpdate(generics.UpdateAPIView):
    serializer_class = ComplaintUpdateSerializer

    def get_queryset(self):
        return Complaint.objects.filter(user=self.request.user.id)