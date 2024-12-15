

# from django.db import models
# from users.models import User  
# class Report(models.Model):
#     SEVERITY_CHOICES = [
#         ('Low', 'Low'),
#         ('Medium', 'Medium'),
#         ('High', 'High'),
#         ('Critical', 'Critical'),
#     ]

#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6)  
#     longitude = models.DecimalField(max_digits=9, decimal_places=6)  
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     image = models.ImageField(upload_to='reports/images/', blank=True, null=True)
#     video = models.FileField(upload_to='reports/videos/', blank=True, null=True)
    
    
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         self.generate_alert()

#     def generate_alert(self):
#         from alert.models import Alert  
#         Alert.objects.create(
#             report=self,
#             message=f"An incident has been reported near this location: {self.title}"
#         )



from django.db import models
from users.models import User

class Report(models.Model):
    CATEGORY_CHOICES = [
        ('Accident de la route', 'Accident de la route'),
        ('Travaux en cours', 'Travaux en cours'),
        ('Violation de feu rouge', 'Violation de feu rouge'),
        ('Embouteillage', 'Embouteillage'),
    ]

    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # New field
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='reports/images/', blank=True, null=True)
    video = models.FileField(upload_to='reports/videos/', blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.generate_alert()

    def generate_alert(self):
        from alert.models import Alert
        Alert.objects.create(
            report=self,
            message=f"An incident has been reported: {self.title} ({self.get_category_display()})"
        )
