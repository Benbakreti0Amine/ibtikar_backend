# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from django.core.mail import send_mail
# from django.conf import settings

# from .models import SOSAlert
# from .serializers import SOSAlertSerializer

# class SendSOSAlertView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = SOSAlertSerializer(data=request.data, context={'request': request})
        
#         if serializer.is_valid():
#             # Save the SOS alert
#             sos_alert = serializer.save()
            
#             # Prepare email content
#             subject = 'URGENT: SOS ALERT'
#             message = f"""
#             EMERGENCY SOS ALERT

#             User: {request.user.username}

#             Location Details:
#             Latitude: {sos_alert.latitude}
#             Longitude: {sos_alert.longitude}
#             Altitude: {sos_alert.altitude or 'N/A'} meters

#             Timestamp: {sos_alert.timestamp}

#             URGENT ASSISTANCE REQUIRED
#             """
            
#             try:
#                 # Send email to emergency contact
#                 send_mail(
#                     subject,
#                     message,
#                     settings.DEFAULT_FROM_EMAIL,
#                     [settings.EMERGENCY_CONTACT_EMAIL],
#                     fail_silently=False,
#                 )
#             except Exception as e:
#                 # Log the error, but still return success for the user
#                 print(f"Failed to send email: {e}")
            
#             return Response({
#                 'status': 'SOS alert sent successfully',
#                 'alert_id': sos_alert.id
#             }, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import get_user_model
# from django.core.mail import send_mail
# from django.conf import settings

# from .models import SOSAlert

# User = get_user_model()

# class SendSOSAlertView(APIView):
#     def post(self, request):
#         # Get latitude and longitude from request
#         latitude = request.data.get('latitude')
#         longitude = request.data.get('longitude')
#         username = request.data.get('username', f'anonymous_{id(request)}')

#         # Validate required fields
#         if not latitude or not longitude:
#             return Response(
#                 {'error': 'Latitude and longitude are required'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Find or create user
#         try:
#             user, _ = User.objects.get_or_create(
#                 username=username,
#                 defaults={'email': f'{username}@temp.com'}
#             )
#         except Exception as e:
#             return Response(
#                 {'error': f'User creation failed: {str(e)}'},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#         # Create SOS alert
#         try:
#             sos_alert = SOSAlert.objects.create(
#                 user=user,
#                 latitude=latitude,
#                 longitude=longitude
#             )
#         except Exception as e:
#             return Response(
#                 {'error': f'SOS alert creation failed: {str(e)}'},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#         # Send email
#         try:
#             send_mail(
#                 'URGENT: SOS ALERT',
#                 f"""
# EMERGENCY SOS ALERT

# User: {username}

# Location:
# https://www.google.com/maps?q={latitude},{longitude}

# Latitude: {latitude}
# Longitude: {longitude}
# """,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [settings.EMERGENCY_CONTACT_EMAIL],
#                 fail_silently=False,
#             )
#         except Exception as e:
#             print(f"Email sending failed: {e}")

#         return Response({
#             'status': 'SOS alert sent successfully',
#             'alert_id': sos_alert.id
#         }, status=status.HTTP_201_CREATED)



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