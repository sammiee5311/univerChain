from django.shortcuts import render

# attendance model


def check_attendance(request):
    if request.method == 'POST' and request.user.is_staff:
        return render(request, 'attendance/check.html')

    return render(request, 'attendance/authentication_fail.html')
