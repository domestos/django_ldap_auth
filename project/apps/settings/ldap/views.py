from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import LDAPConfigForm
from .models import LdapConfig


from apps.settings.ldap.util.ldap_con import authenticate, test_connect, sync_users
# Create your views here.
class LDAPConfigView(View):
    def get(self, request):
        ldap_config = LdapConfig.objects.all().first()
        if(ldap_config is not None):
                ldap_config.LDAP_PASS = ldap_config.decrypt_pass(ldap_config.LDAP_PASS)
        forms = LDAPConfigForm(instance=ldap_config)
        return render(request, 'ldap/index.html', {'forms':forms})
   
    def post(self, request):
        ldap_config = LdapConfig.objects.all().first()
        bound_forms = LDAPConfigForm(request.POST, instance=ldap_config)
        if bound_forms.is_valid():
                bound_forms.save()
                return redirect('ldap_config_url')

        # if request.POST['test_connect_btn']:
        #     print("run test connect")
        #     return redirect('ldap_config_url')

class LDAPTestConnect(View):
    def get(self, request):
            print("run test connect")
            connect_status = test_connect()
            print(connect_status)
            return redirect('ldap_config_url')
    