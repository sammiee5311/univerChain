from django.shortcuts import render
from .detect_face import FaceRecog

# attendance model


def check_attendance(request):
    if request.method == 'POST' and request.user.is_staff:
        current_class = request.POST['class']
        face_recog_attendance = FaceRecog(current_class=current_class)

        # students = models.objects.filter(class=current_class)
        # students = [None]
        # face_recog_attendance.start_face_recog(students, show=False)

        return render(request, 'attendance/check.html')

    return render(request, 'attendance/authentication_fail.html')
