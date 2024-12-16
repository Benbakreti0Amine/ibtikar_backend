


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import User


from alert.utils import calculate_distance, notify_nearby_users  
from report.models import Report  


class UpdateLocationView(APIView):
    permission_classes = [] 

    def post(self, request):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        user_id = request.data.get('user_id', None)  

        # Check if latitude and longitude are provided
        if latitude is None or longitude is None:
            return Response({"error": "Latitude and Longitude are required."}, status=400)

        if request.user.is_authenticated:
            # Get the currently authenticated user
            user = request.user
        elif user_id:
            # If user is not logged in, we will try to use the user_id from the request
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=404)
        else:
            return Response({"error": "User is not authenticated and no user_id was provided."}, status=400)

        # Update the user's location in the database
        user.latitude = latitude
        user.longitude = longitude
        user.save()

        
        self.compare_user_location_with_reports(user)
        return Response({"message": "Location updated successfully"})
    
    def compare_user_location_with_reports(self, user):
        print(f"Entering compare_user_location_with_reports for user ")

        # Retrieve reports from the database that have latitude and longitude
        print(f"Comparing location for user {user.id} with reports...")

        reports = Report.objects.filter(latitude__isnull=False, longitude__isnull=False)
     

        # Loop through each report and check if the user is within range
        for report in reports:
            distance = calculate_distance(user.latitude, user.longitude, report.latitude, report.longitude)
            
            print(f"Distance to report {report.id}: {distance} km")
         
            # If the user is within a certain radius (e.g., 5 km) of the report, notify the user
            if distance <= 5.0:  # 5 km radius
                self.notify_user_about_nearby_report(user, report)

    def notify_user_about_nearby_report(self, user, report):
        # Send a message to the user notifying them about the nearby report
        message = f"New report nearby: {report.title} at {report.latitude}, {report.longitude}"
        print(f"Notifying user {user.id} about report {report.id}")
       
        # Notify the user and others who are near the report (using your notification system)
        notify_nearby_users(report)

