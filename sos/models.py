from django.db import models
from django.conf import settings

class SOSAlert(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sos_alerts'
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"SOS Alert by {self.user.username} at {self.timestamp}"