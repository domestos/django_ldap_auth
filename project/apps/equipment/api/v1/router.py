# Як правило, замість того, щобо реєструвати кожне view в urlpatterns, ми реєструємо viewset в класі router, який автоматично визначає для нас urlconf.
# REST framework надає маршрутезатори для стандартних операцій create/retrieve/update/destroy,

from rest_framework import routers
from .viewset import UserViewSet, LocationViewSet, EquipmentTypeViewSet, EquipmentViewSet

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('location', LocationViewSet)
router.register('type', EquipmentTypeViewSet)
router.register('equipment', EquipmentViewSet)
