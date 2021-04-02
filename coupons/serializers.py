from django.db import transaction
from rest_framework import serializers

from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.name')
    class Meta:
        model = Coupon
        fields = ('uuid', 'buyer', 'buyer_name', 'is_spent', 'timestamp', 'spent_timestamp')
