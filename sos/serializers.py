# from rest_framework import serializers
# from .models import SOSAlert

# class SOSAlertSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SOSAlert
#         fields = ['latitude', 'longitude', 'altitude']
        
#     def create(self, validated_data):
#         # Add the current user to the validated data
#         validated_data['user'] = self.context['request'].user
#         return super().create(validated_data)



from rest_framework import serializers
from .models import SOSAlert

class SOSAlertSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = SOSAlert
        fields = ['latitude', 'longitude', 'altitude', 'username']
        
    def create(self, validated_data):
        # Remove username from validated data if present
        validated_data.pop('username', None)
        
        # Use the user from the context (set in the view)
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)