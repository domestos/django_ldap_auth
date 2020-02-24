from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import User
from apps.settings.ldap.util.ldap_con import  sync_users
from .filters import OrderFilter
from apps.equipment.models import Equipment
from apps.accounts.forms import NewUserForm
from .tables import PersonTable
# Create your views here.

class UsersView(View):
    def get(self, request):       
        users=User.objects.all()
       
        my_filter = OrderFilter(request.GET, queryset=users)
        users = my_filter.qs

        table = PersonTable(users)
        table.paginate(page=request.GET.get("page", 1), per_page=25)
        return render(request, 'accounts/users.html',{'users':users, 'my_filter':my_filter, 'table':table} )


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