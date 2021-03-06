from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import User
from apps.settings.ldap.util.ldap_con import  sync_users
from .filters import OrderFilter
from apps.equipment.models import Equipment
from apps.accounts.forms import NewUserForm
from .tables import PersonTable
from django.views.generic import ListView

from django_tables2.views import SingleTableMixin
from django_tables2 import SingleTableView
from django_filters.views import FilterView

# Create your views here.

# class UsersView(View):
#     def get(self, request):       
#         users=User.objects.all()
       
#         my_filter = OrderFilter(request.GET, queryset=users)
#         users = my_filter.qs

#         table = PersonTable(users)
#         # table.order_by = 'id'
#         table.paginate(page=request.GET.get("page", 1), per_page=10)
#         return render(request, 'accounts/users.html',{'users':users, 'my_filter':my_filter, 'table':table} )



class UsersView(SingleTableMixin, FilterView):
    model = User
    table_class = PersonTable
   
    filterset_class = OrderFilter
    template_name = 'accounts/users.html'

   
    # def get(self, request):       
    #     users=User.objects.all()
       
    #     my_filter = OrderFilter(request.GET, queryset=users)
    #     users = my_filter.qs

    #     table = PersonTable(users)
    #     # table.order_by = 'id'
    #     table.paginate(page=request.GET.get("page", 1), per_page=10)
    #     return render(request, 'accounts/users.html',{'users':users, 'my_filter':my_filter, 'table':table} )



class UserDetailView(View):
    def get(self, request, username):       
        user = get_object_or_404(User, username=username )
        history_e = Equipment.history.filter(user=user).distinct().order_by("-history_date")
        history_u =  user.history.all()
        equipments = Equipment.objects.filter(user=user).order_by("device_type")
        return render(request, 'accounts/user_detail.html',{'user':user, 'equipments':equipments, "history_u":history_u,"history_e":history_e} )


class NewUserView(View):   
    def get(self, request):
        context = {}
        forms = NewUserForm()
        return render(request, 'accounts/new_user.html', {'forms':forms})

    def post(self, request):
        #save user from forms
        context = {}
        forms = NewUserForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('users_url')
        else:
            return render(request, 'accounts/new_user.html', {'forms':forms})



def sync_ldap_users(request):
    print("RUN SYNC")
    sync_users()
    return redirect('users_url')


def view_404(request,  *args, **kwargs):
    return render(request, 'accounts/page_404.html')
