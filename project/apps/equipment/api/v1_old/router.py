# Як правило, замість того, щобо реєструвати кожне view в urlpatterns, ми реєструємо viewset в класі router, який автоматично визначає для нас urlconf.
# REST framework надає маршрутезатори для стандартних операцій create/retrieve/update/destroy,

from rest_framework import routers
from .viewset import PersonViewSet, LocationViewSet, TypeDeviceViewSet, DiveceViewSet

router = routers.DefaultRouter()
router.register('person', PersonViewSet)
router.register('location', LocationViewSet)
router.register('type', TypeDeviceViewSet)
router.register('device', DiveceViewSet)
