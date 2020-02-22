from .views import *
from django.urls import path


urlpatterns = [
    path('', LDAPConfigView.as_view(), name='ldap_config_url'),
    path('test_connect', LDAPTestConnect.as_view(), name='ldap_test_connect_url'),

    
 
]