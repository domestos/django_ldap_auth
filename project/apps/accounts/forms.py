from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .models import User as Profile

#
class NewUserForm(UserCreationForm):
    """ LDAP Credetials form """
   
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name',  'department', 'is_staff',   'password1',  'password2']
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Username"}),
        #     'first_name': forms.TextInput(attrs={'class': 'form-control',  'id': '',  'placeholder': ""}),
        #     'last_name': forms.TextInput(attrs={'class': 'form-control',  'id': '',  'placeholder': ""}),
        #     'department': forms.TextInput(attrs={'class': 'form-control',  'id': '',  'placeholder': ""}),
        #     'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input', "type": "checkbox"}),
        #     'password1': forms.TextInput(attrs={'class': 'form-control', 'type':'password',}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control', 'type':'password',}), 
        # }
