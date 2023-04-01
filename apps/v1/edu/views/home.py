from django.shortcuts import render, redirect
from django.http.response import Http404


def kutish_zali(request):
    if request.user.role == 'student' and request.user.is_verified:
        return redirect('student_dashboard')
    return render(request, 'edu/student/kutish_zali.html')

def home(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('user_login')
    elif user.role == 'teacher':
        return redirect('teacher_dashboard')
    elif user.role == 'student':
        if not user.is_verified:
            return redirect('kutish_zali')
        return redirect('student_dashboard')
    elif user.role == 'administrator':
        return redirect('administrator_dashboard')
    raise Http404()
