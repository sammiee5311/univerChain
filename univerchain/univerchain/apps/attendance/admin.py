from django.contrib import admin

from .models import Attendance, UniversityClass

admin.site.register(UniversityClass)
admin.site.register(Attendance)
