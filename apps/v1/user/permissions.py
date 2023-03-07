from django.shortcuts import redirect
from django.http.response import Http404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin

from apps.v1.user.enums import UserRole

class UserAuthenticateRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if self.request.user.role == 'student':
            if not self.request.user.is_verified:
                return redirect('kutish_zali')
            if request.path != '/student/dashboard/':
                raise Http404
            return super().dispatch(request, *args, **kwargs)
        
        if self.request.user.role == 'teacher':
            if request.path != '/teacher/dashboard/':
                raise Http404
            return super().dispatch(request, *args, **kwargs)
        
        if self.request.user.role == 'admin':
            if request.path != '/admin/dashboard/':
                raise Http404
            return HttpResponse(f"'admin' bo'limi ustida ish olib borilmoqda")
        
        if self.request.user.role == 'super_admin':
            if request.path != '/super_admin/dashboard/':
                raise Http404
            return HttpResponse(f"'Super admin' bo'limi ustida ish olib borilmoqda")

        return super().dispatch(request, *args, **kwargs)