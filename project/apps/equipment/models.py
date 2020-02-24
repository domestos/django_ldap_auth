from django.db import models
from simple_history.models import HistoricalRecords
from apps.accounts.models import User
from django.urls import reverse
# Create your models here.

#=================__LOCATION__=========================
class Location(models.Model):
    name = models.CharField(max_length=250, unique=True, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

#=================__EQUIPMET_TYPE__========================
class EquipmentType(models.Model):
    name = models.CharField(max_length=250, unique=True, blank= True )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Type of Equipment'
        verbose_name_plural = 'Type of Equipments'

#=================__EQUIPMENT__=========================
class Equipment(models.Model):
    options = (('IN_USE','IN_USE'),('SPARE','SPARE'),('BROKEN','BROKEN'),("DISPOSED",'DISPOSED'))
    status = (( 0, "find me"), (1 , "Found"))   
    date_of_purchase = models.DateField('date_of_purchase',blank=True, null=True)
    host_name = models.CharField('host_name', max_length=255, null=True, blank=True)
    inventory_number = models.CharField(max_length=50, unique=True)
    model = models.CharField('model', max_length=255,blank=True, null=True )
    serial_number = models.CharField('serial_number', max_length=255, blank=True, null=True )
    part_number = models.CharField('part_number', max_length=255,blank=True, null=True )
    memory = models.CharField('memory', max_length=255, null=True,blank=True )
    qr_id = models.CharField('qr_id', max_length=255, blank=True, null=True )
    state = models.CharField('state', choices = options,default='SPARE', max_length=255,blank=True, null=True  )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    device_type = models.ForeignKey(EquipmentType, on_delete=models.PROTECT)
    description = models.TextField('description',blank=True, null=True)
    status_inventory = models.IntegerField('status_inventory', choices = status, default='0',  blank=True, null=True  )
    history = HistoricalRecords(related_name='history_inventory')

    def __str__(self):
        return self.inventory_number

    def get_absolute_url(self):
        return reverse("update_equipment_url", kwargs={'pk':self.pk} )

    def save_without_historical_record(self, *args, **kwargs):
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret
        
    class Meta:
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipments'
