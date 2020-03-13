from .views import *
from django.urls import path


urlpatterns = [
    path('', QRCodeConfigView.as_view(), name='qrcode_config_url'),
   

    
 
]