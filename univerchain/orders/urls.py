# mypy: ignore-errors

from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.add, name='add'),
]
