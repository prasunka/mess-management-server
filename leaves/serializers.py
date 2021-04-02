from rest_framework import serializers
from datetime import datetime, timedelta
from .models import Leave

class LeaveListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name')
    end_date = serializers.ReadOnlyField(source='get_end_date')

    class Meta:
        model = Leave
        fields = ('id', 'user', 'user_name', 'applied_date', 'approved_date', 'is_approved',
                'commencement_date', 'body', 'duration', 'end_date')

class LeaveCreateSerializer(serializers.ModelSerializer):
    end_date = serializers.DateField(source='get_end_date')

    class Meta:
        model = Leave
        fields = ('commencement_date', 'body', 'end_date')
    
    def create(self, validated_data):
        try:
            end_date = datetime.strptime(self.context['request'].data.get('end_date'), "%Y-%m-%d").date()
        except:
            serializers.ValidationError("Invalid end_date")
        print(end_date)
        validated_data.pop('get_end_date')
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