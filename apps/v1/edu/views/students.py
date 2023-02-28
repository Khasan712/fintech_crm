from django.shortcuts import render
from apps.v1.edu.models.groups import Group
from apps.v1.edu.models.lessons import Attendance, HomeTask, HomeTaskItem, HomeWork, HomeWorkItem, Lesson
from django.views.generic.base import View
from django.http.response import Http404
from django.http import HttpResponseRedirect


class StudentDashboardView(View):
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
                context['group'] = group.name
                context['page'] = 'group'
        if page == 'lesson' and lesson_id:
            lesson = student_lessons.filter(id=lesson_id).first()
            if not lesson:
                return Http404
            homework = self.get_homework_queryset().filter(student_id=student.id, lesson_id=lesson_id).first()
            if homework:
                context['homework_items'] = self.get_homework_items_queryset().filter(home_work_id=homework.id).values('id', 'uploaded_file')
            context['lesson'] = lesson
            context['page'] = 'lesson'
            subject_guide = self.get_hometask_queryset().filter(
                lesson_id=lesson_id, is_subject_guides=True
            ).first()
            subject_hometask = self.get_hometask_queryset().filter(
                lesson_id=lesson_id, is_subject_guides=False
            ).first()
            if subject_guide:
                subject_guide_items = self.get_hometask_items_queryset().filter(home_task_id=subject_guide.id).order_by('-id')
                context['subject_guides'] = subject_guide_items
            if subject_hometask:
                subject_hometask_items = self.get_hometask_items_queryset().filter(home_task_id=subject_hometask.id).order_by('-id')
                context['subject_hometasks'] = subject_hometask_items
            
        return render(request, 'edu/student/dashboard.html', context)
    

    def post(self, request, *args, **kwargs):
        uploaded_files = self.request.FILES.getlist('uploaded_files')
        print(self.request.FILES)
        print(self.request.POST)
        data = self.request.POST
        user = self.request.user
        method = data.get('method')
        lesson_id = data.get('lesson_id')
        if method == 'homework' and lesson_id and uploaded_files:
            homework, _ = HomeWork.objects.get_or_create(student_id=user.id, lesson_id=lesson_id)
            for uploaded_file in uploaded_files:
                item = HomeWorkItem(
                    home_work_id=homework.id,
                    uploaded_file=uploaded_file
                )
                item.save()
            return HttpResponseRedirect(f'?page=lesson&lesson_id={lesson_id}')


