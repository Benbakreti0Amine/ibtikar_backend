# # from django.shortcuts import render


# # from rest_framework.viewsets import ModelViewSet

# # from users.models import User
# # from .models import Report
# # from .serializers import ReportSerializer


# # class ReportViewSet(ModelViewSet):
# #     queryset = Report.objects.all().order_by('-created_at')
# #     serializer_class = ReportSerializer

# #     def perform_create(self, serializer):
# #         user_id = self.request.data.get('user', None)
# #         user = None
# #         if user_id:
# #             user = User.objects.get(id=user_id) 
# #         serializer.save(user=user)












# from django.shortcuts import render
# from django.db.models import F
# from rest_framework.viewsets import ModelViewSet
# from users.models import User
# from .models import Report
# from .serializers import ReportSerializer
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer


# class ReportViewSet(ModelViewSet):
#     queryset = Report.objects.all().order_by('-created_at')
#     serializer_class = ReportSerializer

#     def perform_create(self, serializer):
#         user_id = self.request.data.get('user', None)
#         user = None

#         if user_id:
#             user = User.objects.get(id=user_id)

#         report = serializer.save(user=user)

#         # Send alerts to nearby users
#         self.send_alerts_to_nearby_users(report)

#     def send_alerts_to_nearby_users(self, report):
#         # Get the location of the report
#         report_lat = report.latitude
#         report_long = report.longitude

#         # Define a proximity threshold (e.g., 0.1 for ~10 km)
#         proximity_threshold = 0.1

#         # Find nearby users
#         nearby_users = User.objects.annotate(
#             lat_diff=F('latitude') - report_lat,
#             long_diff=F('longitude') - report_long,
#         ).filter(
#             lat_diff__lte=proximity_threshold,
#             lat_diff__gte=-proximity_threshold,
#             long_diff__lte=proximity_threshold,
#             long_diff__gte=-proximity_threshold,
#         )

#         # Prepare the alert message
#         alert_message = {
#             'type': 'alert',
#             'message': 'New report nearby!',
#             'report_id': report.id,
#             'latitude': report_lat,
#             'longitude': report_long,
#             'severity': report.severity,
#         }

#         # Send WebSocket notifications to all nearby users
#         channel_layer = get_channel_layer()
#         for user in nearby_users:
#             user_group_name = f"user_{user.id}"
#             async_to_sync(channel_layer.group_send)(
#                 user_group_name,
#                 {
#                     'type': 'send_alert',
#                     'message': alert_message,
#                 }
#             )





from django.shortcuts import render
from django.db.models import F
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User
from .models import Report
from .serializers import ReportSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        # Retrieve the user ID and category from the request data
        user_id = self.request.data.get('user', None)
        user = None

        if user_id:
            user = User.objects.get(id=user_id)

        # Save the report with the user and category
        report = serializer.save(user=user)

        # Send alerts to nearby users
        self.send_alerts_to_nearby_users(report)

    def send_alerts_to_nearby_users(self, report):
        # Get the location of the report
        report_lat = report.latitude
        report_long = report.longitude

        # Define a proximity threshold (e.g., 0.1 for ~10 km)
        proximity_threshold = 0.1

        # Find nearby users
        nearby_users = User.objects.annotate(
            lat_diff=F('latitude') - report_lat,
            long_diff=F('longitude') - report_long,
        ).filter(
            lat_diff__lte=proximity_threshold,
            lat_diff__gte=-proximity_threshold,
            long_diff__lte=proximity_threshold,
            long_diff__gte=-proximity_threshold,
        )

        # Prepare the alert message, including the category
        alert_message = {
            'type': 'alert',
            'message': f"New report nearby! ({report.get_category_display()})",
            'report_id': report.id,
            'latitude': report_lat,
            'longitude': report_long,
            'severity': report.severity,
            'category': report.category,
        }

        # Send WebSocket notifications to all nearby users
        channel_layer = get_channel_layer()
        for user in nearby_users:
            user_group_name = f"user_{user.id}"
            async_to_sync(channel_layer.group_send)(
                user_group_name,
                {
                    'type': 'send_alert',
                    'message': alert_message,
                }
            )

    # Custom action to get reports by user_id
    @action(detail=False, methods=['get'], url_path='user-reports')
    def get_reports_by_user(self, request):
        user_id = request.query_params.get('user_id', None)

        if not user_id:
            return Response({"error": "user_id parameter is required"}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        reports = Report.objects.filter(user=user).order_by('-created_at')
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)
