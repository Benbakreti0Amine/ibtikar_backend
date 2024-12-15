
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from .models import SOSAlert

class SendSOSAlertView(APIView):
    def post(self, request):
        # Extract required information
        name = request.data.get('name', 'Unknown User')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        # Validate required fields
        if not latitude or not longitude:
            return Response(
                {'error': 'Latitude and longitude are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Send email
        try:
            send_mail(
                'URGENT: SOS ALERT',
                f"""
EMERGENCY SOS ALERT

User: {name}

Location:
https://www.google.com/maps?q={latitude},{longitude}

Latitude: {latitude}
Longitude: {longitude}
""",
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMERGENCY_CONTACT_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to send email: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            'status': 'SOS alert sent successfully'
        }, status=status.HTTP_201_CREATED)