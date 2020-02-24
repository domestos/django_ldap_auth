from django.shortcuts import render, redirect
from django.views import View
from .models import Equipment
from .forms import NewDeviceForm
from django.shortcuts import get_object_or_404

# Create your views here.
class EquipmentView(View):
    def get(self, request):
        equipments = Equipment.objects.all()
        return render(request, 'equipment/equipments.html',{'equipments':equipments})

class NewEquipmentView(View):

    def get(self, request):
        form = NewDeviceForm()
        return render(request, 'equipment/new_device.html', {'form':form})

    def post(slef, request):
        bound_form = NewDeviceForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('equipment_url')
        else:
            return render(request, 'equipment/new_device.html',  {'form':bound_form})



class UpdateEquipmentView(View):
    def get(self, request, pk):       
        equipment = get_object_or_404(Equipment, pk=pk)
        bound_form = NewDeviceForm(instance=equipment)
        history_e =  equipment.history.all()
        # history_e = Equipment.history.filter(equipment=pk)
        return render(request, 'equipment/update_device.html',{'equipment':equipment, 'form':bound_form, 'history_e':history_e})

    def post(self, request, pk):
        equipment = get_object_or_404(Equipment, pk=pk)
        bound_form = NewDeviceForm(request.POST, instance=equipment)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('update_equipment_url', pk)
        else:
            return render(request, 'equipment/update_device.html',  {'form':bound_form})

