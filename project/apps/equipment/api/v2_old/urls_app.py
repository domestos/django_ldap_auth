from django.urls import path
from .viewset import PersonViewSet, LocationViewSet, TypeDeviceViewSet, DeviceViewSet
app_name = "inventory"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('person/<int:pk>', PersonViewSet.as_view()),
    path('person', PersonViewSet.as_view()),
    
    path('location/<int:pk>', LocationViewSet.as_view()),
    path('location', LocationViewSet.as_view()),
    
    path('type_device', TypeDeviceViewSet.as_view()),
    path('type_device/<int:pk>', TypeDeviceViewSet.as_view()),

    path('device', DeviceViewSet.as_view()),
    path('device/<int:pk>/', DeviceViewSet.as_view()),
]
