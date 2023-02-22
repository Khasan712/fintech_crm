from functools import wraps
from django.shortcuts import redirect


def isAuthenticated(func):
    @wraps(func)
    def check_user_authenticate(request):
        if not request.user.is_authenticated or request.user.role != 'student':
            return redirect('user_login')
        return func(request)
    return check_user_authenticate