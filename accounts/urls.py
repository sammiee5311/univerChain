from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import LoginForm, PasswordResetConfirm, PassWordResetForm

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html',
                                                form_class=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
            template_name='accounts/user/password_reset.html',
            success_url='password_reset_email_confirm',
            email_template_name='accounts/user/password_reset_email.html',
            form_class=PassWordResetForm),
         name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/user/password_reset_confirm.html',
            success_url='/accounts/password_reset_complete/',
            form_class=PasswordResetConfirm),
         name='password_reset_confirm'),
    path('password_reset/password_reset_email_confirm/',
         TemplateView.as_view(template_name='accounts/user/password_reset_success.html'),
         name='password_reset_done'),
    path('password_reset_complete/',
         TemplateView.as_view(template_name='accounts/user/password_reset_success.html'),
         name='password_reset_complete'),

    path('profile/edit/', views.edit_info, name='edit_info'),
    path('profile/delete/', views.delete, name='delete'),
    path('profile/delete_success', TemplateView.as_view(template_name='accounts/user/delete_success.html'),
         name='delete_success')
]
