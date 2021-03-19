from django.db import transaction
from rest_framework import serializers

from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('uuid', 'buyer', 'is_spent', 'timestamp', 'spent_timestamp')
