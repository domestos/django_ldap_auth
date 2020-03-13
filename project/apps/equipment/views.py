from django.shortcuts import render, redirect
from django.views import View
from .models import Equipment
from .forms import NewDeviceForm
from django.shortcuts import get_object_or_404
from .filters import EquipmentFilter
from .tables import EquipmentTable

from django.contrib import messages
import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin
from django_tables2 import SingleTableView
from django_filters.views import FilterView


from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

from apps.equipment.qr_generator import run_generate_qr_code
# Create your views here.
class EquipmentView(ExportMixin, SingleTableMixin, FilterView):
    model = Equipment
    table_class = EquipmentTable   
    # export_trigger_param ='xls'
    export_formats = ['csv','json' ,'xlsx']
    export_name ="equipments"
    filterset_class = EquipmentFilter
    template_name = 'equipment/equipments.html'
    exclude_columns = ("selected_rows", )
    
    

    

def  equipment_action(request):
    print("RUN ACTION")
    # print(request.COOKIES )
    selected_rows=request.COOKIES.get('selected')
    # print(selected_rows)
    action = request.POST.get('action')
    # arr = [request.POST.get(key) for key in request.POST.keys() if u'check' in key]
  
    # print(request.POST)
    # sqs = Equipment.objects.filter(pk=selected_rows)
    # print(sqs)
    if action == u'print_qrcode':
        #  rows_updated = qs.update(status=u'done', doneDateTime=datetime.now())
        print("You selected -",  len(selected_rows.split(',')), " rows")
        items =selected_rows.split(',')
        eqs = Equipment.objects.filter(pk__in=items)
        print(eqs)
        run_generate_qr_code(eqs)
        from django.shortcuts import render
        return render(request, 'equipment/print_qr.html', {
                'items': eqs,
        })
       
        msg = u'Количество заявок, отмеченных как исполненные - {}.'
        print(msg)
    # elif action == u'cancel':
    #     rows_updated = qs.update(status=u'cancel', doneDateTime=None)
    #     msg = u'Количество заявок, отмеченных как отменённые - {}.'
    return redirect('equipment_url')




    # def get(self, request):
    #     equipments = Equipment.objects.all()
    #     return render(request, 'equipment/equipments.html',{'equipments':equipments})

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


class DeleteEquipmentHistory(View):
    def get(self, request, e_pk, h_pk):
        history_e = Equipment.history.filter(pk=h_pk)
        if  history_e.delete():
                messages.success(request, "History record was deleted.", extra_tags='alert-success')
        return redirect('update_equipment_url', e_pk)