# alerts/utils.py
from math import radians, cos, sin, sqrt, atan2
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from users.models import User

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of Earth in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def notify_nearby_users(report):
    radius = 5.0  # Radius in kilometers
    channel_layer = get_channel_layer()

    users = User.objects.exclude(latitude=None, longitude=None)
    for user in users:
        distance = calculate_distance(report.latitude, report.longitude, user.latitude, user.longitude)
        if distance <= radius:
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}",
                {
                    "type": "send_alert",
                    "message": f"New report nearby: {report.title}",
                },
            )
