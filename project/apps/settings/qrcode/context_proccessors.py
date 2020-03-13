
from .models import QRcodeConfig
 
 
def load_settings(request):
    return {'qrcode_settings': QRcodeConfig.load()}