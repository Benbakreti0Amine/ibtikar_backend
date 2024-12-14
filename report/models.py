from django.db import models

class Report(models.Model):
    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]


    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # Latitude field
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # Longitude field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='reports/images/', blank=True, null=True)
    video = models.FileField(upload_to='reports/videos/', blank=True, null=True)



    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.generate_alert()

    def generate_alert(self):
        from alert.models import Alert  # Import to avoid circular dependency
        Alert.objects.create(
            report=self,
            message=f"An incident has been reported near this location: {self.title}"
        )

