from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.commons.decorators import isAuthenticated
from apps.commons.the_same_fields import get_the_same_fields
from apps.v1.edu.models.groups import Group
from apps.v1.edu.models.lessons import Lesson
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.db.models import Count
from django.http.response import Http404


class StudentDashboardView(View):
    def get(self, request, *args, **kwargs):
        page = self.request.GET.get('page')
        group_id = self.request.GET.get('group_id')
        lesson_id = self.request.GET.get('lesson_id')
        
        
        student = request.user        
        student_groups = Group.objects.select_related('course', 'teacher').filter(
            group_of_student__student_id=student.id
        )
        student_lessons = Lesson.objects.select_related('group', 'creator', 'updater', 'deleter')
        groups = student_groups.values('id', 'name')        
        
        context = {
            'user': student,
            'groups': groups,
            'page': 'dashboard',
        }

        if page == 'group' and group_id:
            group = student_groups.filter(id=group_id).first()
            if group:
                group_lessons = student_lessons.filter(
                    group_id=group_id).order_by('-id').values('id', 'creator__first_name', 'lesson_number', 'created_at', 'start_time', 'end_time', 'status')
                context['lessons'] = group_lessons
                context['page'] = 'group'
        if page == 'lesson' and lesson_id:
            lesson = student_lessons.filter(id=lesson_id).first()
            if not lesson:
                return Http404
            context['lesson'] = lesson
            context['page'] = 'lesson'
        return render(request, 'edu/student/dashboard.html', context)
    




# @isAuthenticated
# def student_dashboard(request):
#     student = request.user
#     student_groups = Group.objects.select_related('course', 'teacher').filter(
#         group_of_student__student_id=student.id
#     ).values('id', 'name')

#     context = {
#         'user': student,
#         'groups': student_groups
#     }

#     return render(request, 'edu/student/dashboard.html', context)


# @isAuthenticated
def student_group(request, pk):
    student = request.user
    student_group = Group.objects.select_related('course', 'teacher').filter(
        group_of_student__student_id=student.id, id=pk
    ).first()
    if student_group:
        student_group = Lesson.objects.select_related('group').filter(group_id=pk).order_by('-id')

    context = {
        'user': student,
        'lessons': student_group
    }

    return render(request, 'edu/student/group.html', context)


