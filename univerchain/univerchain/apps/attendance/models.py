from django.db import models
from univerchain.apps.accounts.models import MyUser


class UniversityClass(models.Model):
    name = models.CharField(max_length=50, blank=False)
    date = models.BinaryField(blank=False)
    description = models.CharField(max_length=128, blank=True)
    start_time = models.TimeField(u"From", blank=False)
    end_time = models.TimeField(u"To", blank=False)

    class Meta:
        verbose_name_plural = "Classes"

    def __str__(self):
        return str(self.name)


class Attendance(models.Model):
    student = models.ForeignKey(MyUser, related_name="student", on_delete=models.CASCADE)
    class_name = models.ForeignKey(UniversityClass, related_name="class_name", on_delete=models.CASCADE)
    time = models.TimeField(blank=True)
    is_attended = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.student)
