from django.db import models



class Alert(models.Model):
    report = models.OneToOneField('report.Report', on_delete=models.CASCADE, related_name='alert')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for Report: {self.report.title}"
