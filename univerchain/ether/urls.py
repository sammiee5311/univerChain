from django.urls import path

from . import views

app_name = 'univercoin'

urlpatterns = [
    path('', views.check_univercoin, name='check_univercoin'),
]
