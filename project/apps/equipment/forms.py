from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminDateWidget
from .models import Equipment, Location
from apps.accounts.models import User
from django_select2.forms import Select2MultipleWidget, Select2Widget
from django_select2.forms import ModelSelect2MultipleWidget
# #
# class MyForm(forms.Form):
#     things = ModelMultipleChoiceField(queryset=Location.objects.all(), widget=Select2MultipleWidget)


class NewDeviceForm(forms.ModelForm):
    """ LDAP Credetials form """
    # date_of_purchase = forms.DateField(widget=AdminDateWidget)
    # location = forms.ModelMultipleChoiceField(queryset=Location.objects.all(), widget=Select2MultipleWidget)
    location = forms.ModelChoiceField(queryset=Location.objects.all(), widget=Select2Widget)
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=Select2Widget)
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
