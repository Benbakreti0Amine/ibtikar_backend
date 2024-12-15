from django.db import models

# Create your models here.
from django.db import models

class SOSAlert(models.Model):
    user_id = models.IntegerField()  # The user ID of the person sending the SOS alert
    username = models.CharField(max_length=255)  # The name of the person sending the alert
    latitude = models.FloatField()  # Latitude of the user's location
    longitude = models.FloatField()  # Longitude of the user's location
    message = models.TextField()  # The message or description of the situation
    sent_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the SOS alert was sent
    resolved = models.BooleanField(default=False)  # Flag to mark if the alert has been resolved

    def __str__(self):
        return f"SOS Alert from {self.username} at {self.sent_at}"

    class Meta:
        verbose_name = "SOS Alert"
        verbose_name_plural = "SOS Alerts"
