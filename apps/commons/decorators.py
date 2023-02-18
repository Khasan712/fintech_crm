from functools import wraps
from django.shortcuts import redirect


def isAuthenticated(func):
    @wraps(func)
    def _wrapped_view(request, *args, **kwargs):
        print(request.user.is_authenticated)
        return func(request, *args, **kwargs)