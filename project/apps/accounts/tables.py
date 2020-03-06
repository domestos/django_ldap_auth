import django_tables2 as tables
from django_tables2_column_shifter.tables import ColumnShiftTable

from django.utils.safestring import mark_safe

from django_tables2.utils import Accessor, AttributeDict
from django.utils.html import format_html



from .models import User

from django.db.models.functions import Length

class PersonTable(ColumnShiftTable):
    username = tables.LinkColumn(order_by="username")
    # action =tables.LinkColumn(orderable=False)
    
    # when_created = tables.DateTimeColumn(format='d/m/Y h:m' , order_by="when_created")
    # when_changed= tables.DateTimeColumn(format='d/m/Y h:m')
    # check = MaterializeCheckColumn(accessor='id')
  
    class Meta:
        model = User
        template_name = "django_tables2/bootstrap.html"
        # add class="paleblue" to <table> tag
        attrs = {}
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'department', 'when_created','when_changed', 'is_active')
        # per_page: 10
    
    # def order_username(self, queryset, is_descending):
    #     print("RUN ORDER")
    #     queryset = queryset.annotate(ength=Length("username")
    #     ).order_by(("-" if is_descending else "") + "length")
    #     return (queryset, True)