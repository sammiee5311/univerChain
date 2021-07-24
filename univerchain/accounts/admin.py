from django.contrib import admin

from .models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "ethereum_account")
    list_display_links = ("id", "username")
    list_per_page = 25


admin.site.register(MyUser, MyUserAdmin)
