from django.db import models

from accounts.models import myuser

class Class(models.Model):
    name = models.CharField(max_length=50, blank=False)
    date = models.BinaryField(blank=False)
    description = models.CharField(max_length=128, blank=True)
    start_time = models.TimeField(u"From", blank=False)
    end_time  = models.TimeField(u"To", blank=False)

    class Meta:
        verbose_name_plural = 'Classes'


class Attendance(models.Model):
    student = models.ForeignKey(myuser, related_name='student',
                                on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, related_name='class',
                                 on_delete=models.CASCADE)
    time = models.TimeField(blank=True)
    is_attended = models.BooleanField(default=False)
