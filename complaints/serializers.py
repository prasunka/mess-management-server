from rest_framework import serializers

from .models import Complaint

class ComplaintListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name')
    class Meta:
        model = Complaint
        fields = ('id', 'user', 'user_name', 'title', 'body', 'applied_date', 'media', 'resolved', 'resolved_date')

class ComplaintCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ('title', 'body', 'media',)

    def create(self, validated_data):
        complaint = Complaint(**validated_data)
        complaint.user = self.context['request'].user
        complaint.save()
        return complaint

class ComplaintUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ('resolved',)