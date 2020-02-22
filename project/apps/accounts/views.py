from django.shortcuts import render
from django.views import View

# Create your views here.

class UsersView(View):
    def get(self, request):
        return render(request, 'accounts/index.html')

