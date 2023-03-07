from django.urls import path
from apps.v1.edu.views import students, teachers, home

# Student
urlpatterns = [
    path('', home.home, name='home'),
    path('fintech-hub/', home.kutish_zali, name='kutish_zali'),
    path('student/dashboard/', students.StudentDashboardView.as_view(), name='student_dashboard'),
    path('teacher/dashboard/', teachers.TeacherDashboardView.as_view(), name='teacher_dashboard'),
]


