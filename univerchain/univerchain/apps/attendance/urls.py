from django.urls import path

from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.check_attendance, name='check_attendance')
]
