from datetime import datetime
from apps.v1.edu.forms import teachers
from django.shortcuts import render, redirect
from django.urls import reverse
from apps.v1.edu.models.groups import Group, GroupStudent
from apps.v1.edu.models.lessons import Lesson
from django.views.generic.base import View
from django.http.response import Http404, HttpResponse
from django.http import HttpResponseRedirect


class TeacherDashboardView(View):

    def get_group_queryset(self):
        return Group.objects.select_related('course', 'teacher', 'creator', 'updater', 'deleter')
    
    def get_lesson_queryset(self):
        return Lesson.objects.select_related('group', 'creator', 'updater', 'deleter')
    
    def get_group_students(self):
        return GroupStudent.objects.select_related(
            'student', 'group', 'creator', 'updater', 'deleter'
        )

    def get(self, request, *args, **kwargs):
        teacher = request.user
        page = self.request.GET.get('page')
        group_id = self.request.GET.get('group_id')
        lesson_id = self.request.GET.get('lesson_id')

        teacher_groups = self.get_group_queryset().filter(teacher_id=teacher.id)
        teacher_lessons = self.get_lesson_queryset()
        context = {
            'user': teacher,
            'page': 'dashboard',
            'groups': teacher_groups.values('id', 'name')
        }

        # Group page
        if page == 'group' and group_id:
            group = teacher_groups.filter(id=group_id).first()
            if group:
                group_lessons = teacher_lessons.filter(group_id=group_id).order_by('-id').values(
                    'id', 'creator__first_name', 'lesson_number', 'created_at', 'start_time', 'end_time', 'status'
                )
                context['lessons'] = group_lessons
                context['group'] = {
                    'id': group.id,
                    'name': group.name
                }
                context['page'] = 'group'

        #  Lesson page
        if page == 'lesson' and lesson_id:
            lesson = teacher_lessons.filter(id=lesson_id).first()
            if not lesson:
                return Http404
            context['lesson'] = lesson
            context['page'] = 'lesson'
            context['students'] = self.get_group_students().filter(group_id=lesson.group.id).values(
                'id', 'student__first_name', 'student__last_name', 'student__student_type'
            )

        # Students page
        if page == 'group_students' and group_id:
            group = teacher_groups.filter(id=group_id).first()
            if group:
                group_students = self.get_group_students().filter(group_id=group.id).values('student__first_name', 'student__last_name')
                context['group'] = {
                    'id': group.id,
                    'name': group.name
                },
                context['students'] = group_students
                context['page'] = 'group_students'
        return render(request, 'edu/teacher/dashboard.html', context)
    

    def post(self, request, *args, **kwargs):
        creator = self.request.user
        method = self.request.POST.get('method')
        page = self.request.POST.get('page')
        group_id = self.request.POST.get('group_id')
        lesson_id = self.request.POST.get('lesson_id')
        lesson_status = self.request.POST.get('status')

        if method == 'create_lesson' and page and group_id:
            group = self.get_group_queryset().filter(id=group_id, teacher_id=creator.id).first()
            if group:
                create_lesson_form = teachers.CreateLessonForm(self.request.POST)
                if not create_lesson_form.is_valid():
                    raise Http404
                lesson_commit = create_lesson_form.save(commit=False)
                lesson_commit.creator_id = creator.id
                lesson_commit.group_id = group_id
                lesson_commit.save()
                context = {
                    'page':'group',
                    'group_id':group_id
                }
                return self.get(self.request, **context)
        if page == 'update_lesson' and lesson_id:
            lesson = self.get_lesson_queryset().filter(id=lesson_id, creator_id=creator.id).first()
            if lesson:
                if lesson.status == 'started' and lesson_status == 'finished':
                    update_lesson_form = teachers.UpdateLessonForm(self.request.POST or None, instance=lesson)
                    if not update_lesson_form.is_valid():
                        return HttpResponse(update_lesson_form.errors)
                        # pass
                    update_lesson_commit = update_lesson_form.save(commit=True)
                    update_lesson_commit.end_time = datetime.now().time().strftime('%H:%M:%S')
                    update_lesson_commit.save()
                else:
                    update_lesson_form = teachers.UpdateLessonForm(self.request.POST or None, instance=lesson)
                    if not update_lesson_form.is_valid():
                        return HttpResponse(update_lesson_form.errors)
                    update_lesson_form.save()
                context = {
                    'page':'lesson',
                    'lesson_id':lesson_id
                }
                return self.get(self.request, **context)
        # return render(request, 'edu/teacher/dashboard.html')