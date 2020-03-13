"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf.urls import handler404
from apps.equipment.api.v1.router import router as api_equipment



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('equipment/', include('apps.equipment.urls')),
    path('settings/ldap/', include('apps.settings.ldap.urls')),
    path('settings/qrcode/', include('apps.settings.qrcode.urls')),
    

    # path('', include(router.urls)),
    path('api/v1/equipment/', include(api_equipment.urls)),
    # path('api/v2/equipment/', include('apps.equipment.api.v2.urls_app')),
    # rest web auth
    # path('api-auth/', include('rest_framework.urls',namespace='rest_framework'))

]

handler404 = 'apps.accounts.views.view_404'