import pytest


def test_class_name(university_class):
    assert str(university_class) == "physics"


def test_attendance_student_name(attendance):
    assert str(attendance) == "test"
