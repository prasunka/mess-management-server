from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'typeAccount', 'specialRole')
        read_only_fields = ('id','email')

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=100)
    typeAccount = serializers.CharField(max_length=20)
    specialRole = serializers.CharField(required=False, max_length=100, allow_null=True)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.name = self.data.get('name')
        user.typeAccount = self.data.get('typeAccount')
        user.specialRole = self.data.get('specialRole')
        user.is_active = True
        user.save()
        return user
