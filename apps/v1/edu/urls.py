from django.urls import path
from apps.v1.edu.views import students
from apps.v1.edu.views import teachers

# Student
urlpatterns = [
    path('student/dashboard/', students.StudentDashboardView.as_view(), name='student_dashboard'),
    path('teacher/dashboard/', teachers.TeacherDashboardView.as_view(), name='teacher_dashboard'),


    # path('dashboard/', students.student_dashboard, name='student_dashboard'),
    path('group/<int:pk>/', students.student_group, name='student_group'),
]


