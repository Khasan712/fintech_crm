from django.urls import path
from apps.v1.edu.views import students

# Student
urlpatterns = [
    path('dashboard/', students.student_dashboard, name='student_dashboard')
]
