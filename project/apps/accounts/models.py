from django.db import models
from django.utils import timezone
from django.urls import reverse
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # def __init__(self):
    #     AbstractUser.__init__(self)

    department = models.CharField(max_length=150, blank=True)
    when_created = models.DateTimeField(default=timezone.now , blank=True)
    when_changed = models.DateTimeField( default=timezone.now, blank=True)
    enabled = models.BooleanField(default=True)
    ldap_user = models.BooleanField(default=False)
    history = HistoricalRecords(related_name='history_profile')

    def __str__(self):
        return self.username
        
    def get_absolute_url(self):
        return reverse("user_detail_url", kwargs={'username':self.username} )