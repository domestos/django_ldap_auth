import django_tables2 as tables
from django_tables2_column_shifter.tables import ColumnShiftTable
from django.utils.safestring import mark_safe
from django_tables2.utils import Accessor, AttributeDict
from django.utils.html import format_html
from django.views.generic import ListView

from django_tables2.export.export import TableExport
from .models import Equipment

from django.db.models.functions import Length


class MaterializeCssCheckboxColumn(tables.CheckBoxColumn):
    def render(self, value, bound_column, record):
        default = {"type": "checkbox", "name": bound_column.name, "value": value}
        if self.is_checked(value, record):
            default.update({"checked": "checked"})

        general = self.attrs.get("input")
        specific = self.attrs.get("td__input")
        attrs = tables.utils.AttributeDict(default, **(specific or general or {}))
        return mark_safe("<p><label><input %s/><span></span></label></p>" % attrs.as_html())

    # @property
    # def header(self):
    #     return "Select"

# class vars(models.Model):
#     idvar=models.IntegerField('Var.ID', primary_key=True)

class EquipmentTable(ColumnShiftTable):
    inventory_number = tables.LinkColumn()
    user= tables.LinkColumn()
    selected_rows=tables.CheckBoxColumn(accessor='pk',attrs = { "th__input": {"onclick": "toggle(this)"}}, orderable=False)
    # def render_selected(self,record):    
    #     if record.selected:
    #         return mark_safe('<input class="nameCheckBox" name="name[]" type="checkbox" checked/>')
    #     else:   
    #         return mark_safe('<input class="nameCheckBox" name="name[]" type="checkbox"/>')
    class Meta:
        model = Equipment
        template_name = "django_tables2/bootstrap.html"
       
        attrs = {}
        fields = ('selected_rows','inventory_number','device_type',    'model', 'serial_number', 'part_number','date_of_purchase','host_name',
         'memory','qr_id', 'state','user', 'user__department','location','description','status_inventory')
        per_page=100
    
    # def order_username(self, queryset, is_descending):
    #     print("RUN ORDER")
    #     queryset = queryset.annotate(ength=Length("username")
    #     ).order_by(("-" if is_descending else "") + "length")
    #     return (queryset, True)