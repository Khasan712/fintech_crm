from datetime import datetime
import pprint
from apps.v1.edu.forms import teachers
from django.shortcuts import render, redirect
from django.urls import reverse
from apps.v1.edu.models.groups import Group, GroupStudent
from apps.v1.edu.models.lessons import Attendance, HomeTask, HomeTaskItem, HomeWork, HomeWorkItem, Lesson
from django.views.generic.base import View
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.v1.user.models import Student

from apps.v1.user.permissions import UserAuthenticateRequiredMixin


class TeacherDashboardView(UserAuthenticateRequiredMixin, View):

    def get_group_queryset(self):
        return Group.objects.select_related('course', 'teacher', 'creator', 'updater', 'deleter')
    
    def get_lesson_queryset(self):
        return Lesson.objects.select_related('group', 'creator', 'updater', 'deleter')
    
    def get_group_students(self):
        return GroupStudent.objects.select_related(
            'student', 'group', 'creator', 'updater', 'deleter'
        )
    
    def get_students_queryset(self):
        return Student.objects.all()
    
    def get_attendance_queryset(self):
        return Attendance.objects.select_related('student', 'lesson')
    
    def get_hometask_queryset(self):
        return HomeTask.objects.select_related('lesson', 'teacher')
    
    def get_hometask_items_queryset(self):
        return HomeTaskItem.objects.select_related('home_task')
    
    def get_homework_queryset(self):
        return HomeWork.objects.select_related('student', 'lesson')
    
    def get_homework_items_queryset(self):
        return HomeWorkItem.objects.select_related('home_work', 'task')
    
    def get(self, request, *args, **kwargs):
        teacher = request.user
        page = self.request.GET.get('page')
        group_id = self.request.GET.get('group_id')
        lesson_id = self.request.GET.get('lesson_id')
        student_id = self.request.GET.get('student_id')

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
            subject_guide = self.get_hometask_queryset().filter(
                lesson_id=lesson_id, teacher_id=teacher.id, is_subject_guides=True
            ).first()
            subject_hometask = self.get_hometask_queryset().filter(
                lesson_id=lesson_id, teacher_id=teacher.id, is_subject_guides=False
            ).first()
            if subject_guide:
                subject_guide_items = self.get_hometask_items_queryset().filter(home_task_id=subject_guide.id).order_by('-id')
                context['subject_guides'] = subject_guide_items
            if subject_hometask:
                subject_hometask_items = self.get_hometask_items_queryset().filter(home_task_id=subject_hometask.id).order_by('-id')
                context['subject_hometasks'] = subject_hometask_items
            context['lesson'] = lesson
            context['page'] = 'lesson'
            context['students'] = self.get_attendance_queryset().filter(lesson_id=lesson.id, lesson__creator_id=teacher.id).values(
                'student__id', 'student__first_name', 'student__last_name', 'student__student_type', 'is_come', 'h_m_percentage'
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
        
        # Student in lesson
        if page == 'student_in_lesson' and student_id:
            student = self.get_students_queryset().filter(student_attendance__student_id=student_id).first()
            if student:
                context['page'] = 'student_in_lesson'
                context['student'] = student
                context['homework_items'] = self.get_homework_items_queryset().filter(home_work__student_id=student_id, home_work__lesson_id=lesson_id)
        return render(request, 'edu/teacher/dashboard.html', context)
    

    def post(self, request, *args, **kwargs):
        creator = self.request.user
        data = self.request.POST
        method = data.get('method')
        page = data.get('page')
        group_id = data.get('group_id')
        lesson_id = data.get('lesson_id')
        lesson_status = data.get('status')
        item_id = data.get('item_id')

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
                group_students = self.get_group_students().filter(group_id=group.id)
                for g_student in group_students:
                    created, _ = Attendance.objects.get_or_create(student_id=g_student.student.id, lesson_id=lesson_commit.id)

                return HttpResponseRedirect(f'?page=group&group_id={group_id}')
            
        if page == 'update_lesson' and lesson_id:
            lesson = self.get_lesson_queryset().filter(id=lesson_id, creator_id=creator.id).first()
            if lesson:
                if lesson.status == 'started' and lesson_status == 'finished':
                    update_lesson_form = teachers.UpdateLessonForm(self.request.POST or None, instance=lesson)
                    if not update_lesson_form.is_valid():
                        return HttpResponse(update_lesson_form.errors)
                    update_lesson_commit = update_lesson_form.save(commit=True)
                    update_lesson_commit.end_time = datetime.now().time().strftime('%H:%M:%S')
                    update_lesson_commit.save()
                else:
                    update_lesson_form = teachers.UpdateLessonForm(self.request.POST or None, instance=lesson)
                    if not update_lesson_form.is_valid():
                        return HttpResponse(update_lesson_form.errors)
                    update_lesson_form.save()
                return HttpResponseRedirect(f'?page=lesson&lesson_id={lesson_id}')
        
        if method == 'create_attendency':
            students_attendance = [

            ]
            students_id = data.get('students_id')
            iscome = bool(data.get('iscome') == 'true')
            h_w_percentage = data.get('h_w_percentage')
            for student_atten in range(len(students_id)):
                print(student_atten)
            for student_id in students_id:
                pass
            lesson = self.get_lesson_queryset().filter(id=lesson_id, creator_id=creator.id).first()
            lesson_students = self.get_attendance_queryset().filter(lesson_id=lesson.id)
            for a_student in students_attendance:
                student_attend = lesson_students.filter(student_id=int(a_student)).first()
                if student_attend:
                    student_attend.is_come = True
                    student_attend.save()
            context = {
                'page':'lesson',
                'lesson_id':lesson_id
            }
            return HttpResponse('Created')
        
        if method == 'subject_guides' and page == 'lesson' and lesson_id:
            subject_guide_text = self.request.POST.get('text')
            uploaded_files = self.request.FILES.getlist('uploaded_file')
            hometask = self.request.POST.get('home_task')
            if not hometask == 'true':
                subject_guide, _ = HomeTask.objects.get_or_create(
                    lesson_id=lesson_id, teacher_id=creator.id, is_subject_guides=True
                )
                if subject_guide:
                    if subject_guide_text:
                        HomeTaskItem.objects.create(home_task_id=subject_guide.id, text=subject_guide_text)
                    if uploaded_files:
                        for uploaded_file in uploaded_files:
                            type_file = uploaded_file.name.split('.')[-1]
                            if type_file in ['mp4', 'mkv']:
                                HomeTaskItem.objects.create(home_task_id=subject_guide.id, uploaded_file=uploaded_file, video=True)
                            else:
                                HomeTaskItem.objects.create(home_task_id=subject_guide.id, uploaded_file=uploaded_file)
            else:
                subject_hometask, _ = HomeTask.objects.get_or_create(
                    lesson_id=lesson_id, teacher_id=creator.id,  is_subject_guides=False
                )
                if subject_hometask:
                    if subject_guide_text:
                        HomeTaskItem.objects.create(home_task_id=subject_hometask.id, text=subject_guide_text)
                    if uploaded_files:
                        for uploaded_file in uploaded_files:
                            type_file = uploaded_file.name.split('.')[-1]
                            if type_file == 'mp4':
                                HomeTaskItem.objects.create(home_task_id=subject_hometask.id, uploaded_file=uploaded_file, video=True)
                            else:
                                HomeTaskItem.objects.create(home_task_id=subject_hometask.id, uploaded_file=uploaded_file)
            
        
        if method == "edit_guides_and_tasks" and item_id:
            pass
        return HttpResponseRedirect(f'?page=lesson&lesson_id={lesson_id}')