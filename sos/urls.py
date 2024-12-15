from django.urls import path
from .views import SOSAlertView

urlpatterns = [
    path('', SOSAlertView.as_view(), name='sos-alert'),
]