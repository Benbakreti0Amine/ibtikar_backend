from rest_framework import serializers
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    report_title = serializers.CharField(source='report.title', read_only=True)

    class Meta:
        model = Alert
        fields = ['id', 'report', 'report_title', 'message', 'created_at']
