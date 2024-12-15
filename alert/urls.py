# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import AlertViewSet

# router = DefaultRouter()
# router.register(r'', AlertViewSet, basename='alert')

# urlpatterns = [
#     path('', include(router.urls)),
# ]


# users/urls.py
from django.urls import path
from .views import UpdateLocationView

urlpatterns = [
    path('update-location/', UpdateLocationView.as_view(), name='update-location'),
]
