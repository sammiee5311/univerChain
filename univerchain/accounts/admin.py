from django.contrib import admin

from .models import myuser


class myuserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'ethereum_account')
    list_display_links = ('id', 'username')
    list_per_page = 25


admin.site.register(myuser, myuserAdmin)
