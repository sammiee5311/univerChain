import pytest
from django.urls import reverse


def test_check_attendance_render(client, admin_user, university_class, attendance):
    user = admin_user
    client.force_login(admin_user)
    response = client.post(reverse("attendance:check_attendance"))

    return response.status_code == 200


def test_check_attendance_authentication_fail(client, university_class, attendance):
    response = client.post(reverse("attendance:check_attendance"))

    return response.status_code == 200
