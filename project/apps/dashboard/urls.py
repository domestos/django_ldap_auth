from .views import *
from django.urls import path

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard_url'),
 
]