from rest_framework import serializers
from datetime import datetime, timedelta
from .models import Leave

class LeaveListSerializer(serializers.ModelSerializer):
    end_date = serializers.ReadOnlyField(source='get_end_date')

    class Meta:
        model = Leave
        fields = ('id', 'applied_date', 'approved_date', 'is_approved',
                'commencement_date', 'body', 'duration', 'end_date')

class LeaveCreateSerializer(LeaveListSerializer):
    def create(self, validated_data):
        try:
            end_date = datetime.strptime(self.context['request'].data.get('end_date'), "%Y-%m-%d").date()
        except:
            serializers.ValidationError("Invalid end_date")
        print(end_date)
        leave = Leave(**validated_data)
        leave.user = self.context['request'].user
        duration = (end_date - validated_data['commencement_date'] + timedelta(days=1)).days
        if(duration > 0):
            leave.duration = duration
        leave.save()
        return leave

class LeaveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ('is_approved',)