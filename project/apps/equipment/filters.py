# https://www.youtube.com/watch?v=G-Rct7Na0UQ
import django_filters
from .models import Equipment
from django_filters import DateTimeFilter , CharFilter , BooleanFilter, AllValuesMultipleFilter
from django.forms.widgets import TextInput, SelectDateWidget, Select, DateTimeInput
from django_select2.forms import Select2MultipleWidget , Select2Widget
class EquipmentFilter(django_filters.FilterSet):

    # CHOICES=(
    #     ('ascending', 'Ascending'),
    #     ('descending', "Descending")
    # )
    # username = CharFilter(field_name='username', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'username'}) )
    # first_name = CharFilter(field_name='first_name', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'first_name'}) )
    # last_name = CharFilter(field_name='last_name', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'last_name'}) )
    # department = CharFilter(field_name='department', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'department'}) )
   
    # ordering = django_filters.ChoiceFilter(label="Ordering by when created", choices=CHOICES, method='filter_by_ordering', widget=Select(attrs={'class':'form-control'}))
    # when_created = DateTimeFilter(label="Date", field_name='when_created', lookup_expr='gte', widget=DateTimeInput(attrs={'class': 'form-control datetimepicker'}) )
    user__department = AllValuesMultipleFilter(
        # queryset=Profile.objects.all().values_list('department', flat=True).distinct(),  Select(attrs={'class':'form-control'})
         widget=Select2MultipleWidget(attrs={'class':'js-example-placeholder-single js-states form-control'})
    )
    class Meta:
        model = Equipment
        fields = {
            'date_of_purchase': ['icontains'],
            'host_name': ['icontains'],
            'inventory_number': ['icontains'],
            'model' : ['icontains'],
            'serial_number': ['icontains'],
            'part_number': ['icontains'],
            'memory': ['icontains'],
            'state': ['icontains'],
            'user__username': ['icontains'],
            # 'user__department': ['icontains'],
        
        }

    
    # def filter_by_ordering(self, queryset, name, value):
    #     expression = 'when_created' if value == 'ascending' else '-when_created'
    #     print(queryset)
    #     return queryset.order_by(expression)











# username = CharFilter(field_name='username', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'username'}) )
#     first_name = CharFilter(field_name='first_name', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'first_name'}) )
#     last_name = CharFilter(field_name='last_name', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'last_name'}) )
#     department = CharFilter(field_name='department', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'department'}) )
   
#     ordering = django_filters.ChoiceFilter(label="Ordering by when created", choices=CHOICES, method='filter_by_ordering', widget=Select(attrs={'class':'form-control'}))
#     when_created = DateTimeFilter(label="Date", field_name='when_created', lookup_expr='gte', widget=DateTimeInput(attrs={'class': 'form-control datetimepicker'}) )
#     is_active = BooleanFilter(field_name='is_active',  )