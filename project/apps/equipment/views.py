from django.shortcuts import render
from django.views import View

# Create your views here.
class EquipmentView(View):
    def get(self, request):
        return render(request, 'equipment/index.html')