from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import LoginForm

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html',
                                                form_class=LoginForm), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('profile/edit/', views.edit_info, name='edit_info'),
    path('profile/delete/', views.delete, name='delete'),
    path('profile/delete_success', TemplateView.as_view(template_name='accounts/user/delete_success.html'),
         name='delete_success')
]
