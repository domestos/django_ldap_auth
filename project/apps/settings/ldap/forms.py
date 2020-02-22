from django import forms
from django.conf import settings
from .models import LdapConfig

#
class LDAPConfigForm(forms.ModelForm):
    """ LDAP Credetials form """
    class Meta:
        model = LdapConfig
        fields = ['LDAP_URL', 'LDAP_USER', 'LDAP_PASS', 'LDAP_BASE_DN','LDAP_AUTH']
        widgets = {
            'LDAP_URL': forms.TextInput(attrs={'class': 'form-control',  'id': 'inputServer',  'placeholder': "IP-Address or Hostname (FQDN)"}),
            'LDAP_USER': forms.TextInput(attrs={'class': 'form-control',  'id': 'inputUser',  'placeholder': "Domain\\User"}),
            'LDAP_PASS': forms.TextInput(attrs={'class': 'form-control', 
                'autocomplete':"new-password",   
                'type':'password',
                'id': 'inputPassword',  'placeholder': "******"}),
            'LDAP_BASE_DN': forms.TextInput(attrs={'class': 'form-control', 'aria-describedby':"inputBaseOU",  'id': 'inputBaseOU',  'placeholder': "Example: ou=base OU,dc=domain,dc=net"}),

        }
