from django.shortcuts import render, redirect
from .models import QRcodeConfig
from .forms import QRcodeConfigForm
from django.views import View
# Create your views here.

class QRCodeConfigView(View):
    def get(self, request):
        qr_code_config = QRcodeConfig.objects.all().first()
        forms  = QRcodeConfigForm(instance=qr_code_config)
        return render(request, 'qrcode/index.html', {'forms': forms})

    def post(self, request):
        qr_code_config = QRcodeConfig.objects.all().first()
        bound_forms = QRcodeConfigForm(request.POST, instance=qr_code_config)
        if bound_forms.is_valid():
            bound_forms.save()
            return redirect('qrcode_config_url')