from django.urls import path
from apps.v1.edu.views import students

# Student
urlpatterns = [
    path('dashboard/', students.StudentDashboardView.as_view(), name='student_dashboard'),


    # path('dashboard/', students.student_dashboard, name='student_dashboard'),
    path('group/<int:pk>/', students.student_group, name='student_group'),
]


