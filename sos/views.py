from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from twilio.rest import Client
from django.conf import settings
from .models import SOSAlert  # Import the SOSAlert model

class SOSAlertView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        username = request.data.get('username')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        if not user_id or not username or not latitude or not longitude:
            return JsonResponse({"error": "Missing required fields."}, status=400)

        # Create and save the SOS alert to the database
        sos_alert = SOSAlert.objects.create(
            user_id=user_id,
            username=username,
            latitude=latitude,
            longitude=longitude,
            message=f"SOS Alert: {username} is in distress at latitude: {latitude}, longitude: {longitude}. Please respond immediately."
        )

        # Send the SOS alert
        self.send_sos_alert(sos_alert.message)

        return JsonResponse({"message": "SOS alert sent successfully!"}, status=200)

    def send_sos_alert(self, message):
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        from_phone = settings.TWILIO_PHONE_NUMBER
        to_phone = settings.POLICE_PHONE_NUMBER

        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone
        )
