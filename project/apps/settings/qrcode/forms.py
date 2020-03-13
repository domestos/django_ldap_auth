from django import forms
from django.conf import settings
from .models import QRcodeConfig

#
class QRcodeConfigForm(forms.ModelForm):
    """ LDAP Credetials form """
    class Meta:
        model = QRcodeConfig
        fields = ['img_width', 'font_size','inventory_margin_top', 'model_visibility', 'model_font_size']
      
