from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import Report
from .serializers import ReportSerializer

class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')  # Order by latest reports
    serializer_class = ReportSerializer
