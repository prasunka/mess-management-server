from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'typeAccount', 'specialRole', 'billingMode')
        read_only_fields = ('id', 'email', 'billingMode')

class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom register serializer for adding new fields and ensuring is_active is True.
    Also removes username from API endpoint.
    """
    username = None
    name = serializers.CharField(max_length=100)
    typeAccount = serializers.CharField(max_length=20)
    specialRole = serializers.CharField(required=False, max_length=100, allow_null=True)
    requestedBillingMode = serializers.CharField(max_length=100, allow_null=True, required=False)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.name = self.data.get('name')
        user.typeAccount = self.data.get('typeAccount')
        user.specialRole = self.data.get('specialRole')
        user.requestedBillingMode = self.data.get('requestedBillingMode')
        user.is_active = True
        user.save()
        return user


class CustomLoginSerializer(LoginSerializer):
    """
    Use default serializer except don't use username
    """

    username = None

class ModeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('requestedBillingMode',)