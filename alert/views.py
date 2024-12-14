from django.shortcuts import render

# Create your views here.


from rest_framework import viewsets, permissions
from geopy.distance import geodesic
from .models import Alert
from .serializers import AlertSerializer

# class AlertViewSet(viewsets.ModelViewSet):
#     queryset = Alert.objects.all()
#     serializer_class = AlertSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user_profile = self.request.user.profile
#         user_location = (float(user_profile.latitude), float(user_profile.longitude))

#         # Define the radius for filtering alerts (e.g., 5 km)
#         ALERT_RADIUS = 5  # in kilometers
#         nearby_alerts = []

#         for alert in Alert.objects.all():
#             report_location = (float(alert.report.latitude), float(alert.report.longitude))
#             distance = geodesic(user_location, report_location).kilometers
#             if distance <= ALERT_RADIUS:
#                 nearby_alerts.append(alert.id)

#         return Alert.objects.filter(id__in=nearby_alerts)


from rest_framework import viewsets, permissions
from .models import Alert
from .serializers import AlertSerializer

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Override to customize the GET response if needed
        return super().list(request, *args, **kwargs)
