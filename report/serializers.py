


from rest_framework import serializers
from .models import Report
from users.models import User

class ReportSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Report
        fields = ['id', 'title', 'description', 'severity', 'category', 
                  'latitude', 'longitude', 'image', 'video', 'user']

    def get_category_choices(self, obj):
        """
        Returns the available category choices for the report.
        """
        return Report.CATEGORY_CHOICES

    def get_localisation(self, obj):
        return {
            "latitude": obj.latitude,
            "longitude": obj.longitude
        }
