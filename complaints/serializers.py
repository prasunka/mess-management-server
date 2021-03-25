from rest_framework import serializers

from .models import Complaint

class ComplaintListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ('id', 'title', 'body', 'media', 'resolved')

class ComplaintCreateSerializer(ComplaintListSerializer):
    def create(self, validated_data):
        complaint = Complaint(**validated_data)
        complaint.user = self.context['request'].user
        complaint.save()
        return complaint

class ComplaintUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ('id', 'resolved')