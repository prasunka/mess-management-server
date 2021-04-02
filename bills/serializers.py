from django.db import transaction
from rest_framework import serializers

from .models import Bill

class BillSerializer(serializers.ModelSerializer):
    month = serializers.ReadOnlyField(source='get_month')
    year = serializers.ReadOnlyField(source='get_year')
    buyer_name = serializers.CharField(source='buyer.name')
    class Meta:
        model = Bill
        fields = ('id', 'buyer', 'buyer_name', 'is_paid', 'bill_from', 'bill_days', 'bill_amount', 'month', 'year')