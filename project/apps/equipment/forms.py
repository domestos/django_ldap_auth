from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminDateWidget
from .models import Equipment

#
class NewDeviceForm(forms.ModelForm):
    """ LDAP Credetials form """
    # date_of_purchase = forms.DateField(widget=AdminDateWidget)
    class Meta:
        model = Equipment
        fields = ['date_of_purchase','inventory_number', 'model', 'serial_number', 'host_name', 'part_number', 'memory', 'user', 'location',  'device_type', 'description']
        # widgets = {
        #     'date_of_purchase': forms.DateTimeInput(attrs={ 'type':'date', 'class': 'form-control vDateField'}),
        #     'inventory_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Username"}),
        #     'host_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Host Name"}),
           
        #     'user': forms.Select(attrs={'class': 'form-control',  'id': '',  'placeholder': ""}),
        #     'location': forms.Select(attrs={'class': 'form-control',  'id': '',  'placeholder': ""}),
        #     'device_type': forms.Select(attrs={'class': 'form-control',  'id': '',  'placeholder': ""}),
            
        #     }
