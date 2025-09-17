from rest_framework import serializers
from .models import Task, WeatherLog

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'status', 
                 'created_at', 'updated_at', 'due_date', 'user']
        read_only_fields = ['created_at', 'updated_at']

class WeatherLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherLog
        fields = '__all__'