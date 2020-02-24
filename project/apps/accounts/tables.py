import django_tables2 as tables
from .models import User

class PersonTable(tables.Table):
    class Meta:
        model = User
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
        fields = ('id', 'username', 'first_name', 'last_name')
       