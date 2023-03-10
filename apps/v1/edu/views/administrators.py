from django.shortcuts import render
from django.views.generic.base import View
from apps.v1.user.models import Student

from apps.v1.user.permissions import UserAuthenticateRequiredMixin


class AdministratorDashboardView(UserAuthenticateRequiredMixin, View):

    def get_students_queryset(self):
        return Student.objects.all()
    
    def get(self, request, *args, **kwargs):
        administrator = self.request.user
        page = self.request.GET.get('page')

        context = {
            "user": administrator,
            'page': "dashboard"
        }

        if not page:
            context.update(
                {
                    "total_students_qty": len(self.get_students_queryset()),
                    "not_verified_students_qty": len(self.get_students_queryset().filter(is_verified=False)),
                    "students_in_groups_qty": len(self.get_students_queryset().filter(
                        is_verified=True, student_in_group__student__isnull=False, student_in_group__student_status="studying"
                    )),
                    "finished_students_qty": len(self.get_students_queryset().filter(
                        is_verified=True, student_in_group__student__isnull=False, student_in_group__student_status="finished"
                    ))
                }
            )
        return render(request, 'edu/administrator/dashboard.html', context)
