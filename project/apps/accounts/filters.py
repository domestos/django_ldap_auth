# https://www.youtube.com/watch?v=G-Rct7Na0UQ
import django_filters
from django import forms
from .models import User as Profile
from django_filters import DateTimeFilter , CharFilter , BooleanFilter, AllValuesMultipleFilter, ModelMultipleChoiceFilter
from django.forms.widgets import TextInput, SelectDateWidget, Select, DateTimeInput
from django_select2.forms import Select2MultipleWidget , Select2Widget
from django_select2.forms import ModelSelect2MultipleWidget

from django_select2 import forms as select2
class OrderFilter(django_filters.FilterSet):

    CHOICES=(
        ('ascending', 'Ascending'),
        ('descending', "Descending")
    )
    # username = CharFilter(field_name='username', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'username'}) )
    # first_name = CharFilter(field_name='first_name', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'first_name'}) )
    # last_name = CharFilter(field_name='last_name', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'last_name'}) )
    # ?department = Select(field_name='department' )
    # position = django_filters.ChoiceFilter(choices=CHOICES, widget=Select2MultipleWidget)

    ordering = django_filters.ChoiceFilter(label="Ordering by when created", choices=CHOICES, method='filter_by_ordering', widget=Select(attrs={'class':'form-control'}))
    # when_created = DateTimeFilter(label="Date", field_name='when_created', lookup_expr='gte', widget=DateTimeInput(attrs={'class': 'form-control datetimepicker'}) )
    is_active = BooleanFilter(label="Active contains", field_name='is_active' )
    # department = ModelMultipleChoiceField(queryset=Profile.objects.all().values('department').distinct())
    # department = django_filters.ModelMultipleChoiceFilter(
        
    #     # queryset=Profile.objects.values_list('department', flat=True).distinct()
    #     queryset=Profile.objects.all().values_list('department', flat=True).distinct(),
    #                                                    widget=forms.CheckboxSelectMultiple
    #     # queryset= Profile.objects.order_by('department').distinct('department')
    # )

    # username = forms.ModelMultipleChoiceField(queryset=Profile.objects.all(), widget=Select2MultipleWidget)
    # department = AllValuesMultipleFilter(  widget=forms.SelectMultiple)

    department = AllValuesMultipleFilter(
        # queryset=Profile.objects.all().values_list('department', flat=True).distinct(),  Select(attrs={'class':'form-control'})
         widget=Select2MultipleWidget(attrs={'class':'js-example-placeholder-single js-states form-control'})
    )
    class Meta:
        model = Profile
        fields = {
            'username': ['icontains'],
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            # 'department' : ['contains'],
            'when_created': ['icontains'],
            
        }

    
    def filter_by_ordering(self, queryset, name, value):
        expression = 'when_created' if value == 'ascending' else '-when_created'
        print(queryset)

        
        return queryset.order_by(expression)











# username = CharFilter(field_name='username', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'username'}) )
#     first_name = CharFilter(field_name='first_name', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'first_name'}) )
#     last_name = CharFilter(field_name='last_name', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'last_name'}) )
#     department = CharFilter(field_name='department', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'department'}) )
   
#     ordering = django_filters.ChoiceFilter(label="Ordering by when created", choices=CHOICES, method='filter_by_ordering', widget=Select(attrs={'class':'form-control'}))
#     when_created = DateTimeFilter(label="Date", field_name='when_created', lookup_expr='gte', widget=DateTimeInput(attrs={'class': 'form-control datetimepicker'}) )
#     is_active = BooleanFilter(field_name='is_active',  )