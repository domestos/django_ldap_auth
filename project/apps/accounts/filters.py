# https://www.youtube.com/watch?v=G-Rct7Na0UQ
import django_filters
from .models import User as Profile
from django_filters import DateTimeFilter , CharFilter , BooleanFilter
from django.forms.widgets import TextInput, SelectDateWidget, Select, DateTimeInput

class OrderFilter(django_filters.FilterSet):

    CHOICES=(
        ('ascending', 'Ascending'),
        ('descending', "Descending")
    )
    # username = CharFilter(field_name='username', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'username'}) )
    # first_name = CharFilter(field_name='first_name', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'first_name'}) )
    # last_name = CharFilter(field_name='last_name', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'last_name'}) )
    # department = CharFilter(field_name='department', lookup_expr='icontains', widget=TextInput(attrs={'class':'form-control','placeholder': 'department'}) )
   
    ordering = django_filters.ChoiceFilter(label="Ordering by when created", choices=CHOICES, method='filter_by_ordering', widget=Select(attrs={'class':'form-control'}))
    # when_created = DateTimeFilter(label="Date", field_name='when_created', lookup_expr='gte', widget=DateTimeInput(attrs={'class': 'form-control datetimepicker'}) )
    is_active = BooleanFilter(label="Active contains", field_name='is_active' )
    class Meta:
        model = Profile
        fields = {
            'username': ['icontains'],
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'department' : ['icontains'],
            'when_created': ['icontains'],
            # 'is_active' : ['icontains'],
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