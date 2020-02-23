from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import User
from apps.settings.ldap.util.ldap_con import  sync_users
from .filters import OrderFilter
from apps.accounts.forms import NewUserForm
# Create your views here.

class UsersView(View):
    def get(self, request):       
        users=User.objects.all()
        my_filter = OrderFilter(request.GET, queryset=users)
        users = my_filter.qs
        return render(request, 'accounts/users.html',{'users':users, 'my_filter':my_filter} )


class UserDetailView(View):
    def get(self, request, username):       
        user = get_object_or_404(User, username=username )
      
        return render(request, 'accounts/user_detail.html',{'user':user} )


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
    sync_users()
    return redirect('users_url')