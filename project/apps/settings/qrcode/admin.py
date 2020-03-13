from django.contrib import admin

# Register your models here.

 
from django.db.utils import ProgrammingError
 

from .models import QRcodeConfig
 
 
# class QRcodeConfigAdmin(admin.ModelAdmin):
#     # Создадим объект по умолчанию при первом страницы SiteSettingsAdmin со списком настроек
#     def __init__(self, model, admin_site):
#         super().__init__(model, admin_site)
#         # обязательно оберните загрузку и сохранение SiteSettings в try catch,
#         # чтобы можно было выполнить создание миграций базы данных
#         try:
#             QRcodeConfig.load().save()
#         except ProgrammingError:
#             pass
 
#     # запрещаем добавление новых настроек
#     def has_add_permission(self, request, obj=None):
#         return False
 
#     # а также удаление существующих
#     def has_delete_permission(self, request, obj=None):
#         return False
 
 
# admin.site.register(QRcodeConfig, QRcodeConfigAdmin)