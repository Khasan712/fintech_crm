from django.shortcuts import render, redirect


def home(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('user_register')
    if user.role == 'teacher':
        return redirect('teacher_dashboard')
    if user.role == 'student':
        return redirect('student_dashboard')
