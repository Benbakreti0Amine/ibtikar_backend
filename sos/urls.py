from django.urls import path
from .views import SendSOSAlertView  # Remove SOSAlertView if it doesn't exist

urlpatterns = [
    path('send-sos/', SendSOSAlertView.as_view(), name='send_sos_alert'),
]