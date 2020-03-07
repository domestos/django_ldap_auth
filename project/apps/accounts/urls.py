from django.contrib.auth import views
from .views import *
from django.urls import path
from django.conf.urls import include, url
urlpatterns = [
    path('sync_ldap_users', sync_ldap_users , name='sync_ldap_users_url'),
    path('', UsersView.as_view(), name='users_url'),
    path('new_user', NewUserView.as_view(), name='new_user_url'),
    path('<str:username>', UserDetailView.as_view(), name='user_detail_url'),
    path('sync_ldap_users', sync_ldap_users , name='sync_ldap_users_url'),
    url(r'^select2/', include('django_select2.urls')),


    
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]