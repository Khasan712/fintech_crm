import pytz
import datetime
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.views.generic.base import View
from django.http.response import Http404
from django.http import HttpResponseRedirect
from apps.v1.edu.models.groups import Group, GroupStudent, StudentProject, StudentProjectsCard
from apps.v1.edu.models.lessons import Attendance, HomeTask, HomeTaskItem, HomeWork, HomeWorkItem, Lesson
from apps.v1.edu.models.presentations import StudentBookPresentation, StudentBookPresentationCard
from apps.v1.user.permissions import UserAuthenticateRequiredMixin
utc=pytz.UTC


class StudentDashboardView(UserAuthenticateRequiredMixin, View):
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
    
    def get_student_projects_card_queryset(self):
        return StudentProjectsCard.objects.select_related("student", "group")
    
    def get_student_projects(self):
        return StudentProject.objects.select_related("project_card")
    
    def get_book_presentation_queryset(self):
        return StudentBookPresentationCard.objects.select_related('student')
    
    def get_book_presentation_item_queryset(self):
        return StudentBookPresentation.objects.select_related("book_card", 'approver')
    
    def get_group_students_queryset(self):
        return GroupStudent.objects.select_related('student', 'group', 'creator', 'updater', 'deleter', 'student_first_lesson')
    
    def get_group_queryset(self):
        return Group.objects.select_related('course', 'teacher', 'creator', 'updater', 'deleter')
    

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

        match page:

            # dashboard
            case None | 'dashboard':
                context['dashboard_statistics'] = {
                    "book_presentation": self.get_book_presentation_queryset().filter(student_id=student.id).first(),
                    "book_presentation_qty": len(self.get_book_presentation_item_queryset().filter(book_card__student_id=student.id, is_aproved=True)),
                    "projects": self.get_student_projects_card_queryset().filter(student_id=student.id)
                }

            # book presentation
            case 'book_presentation':
                book_presentations = self.get_book_presentation_item_queryset().filter(book_card__student_id=student.id).annotate(
                    order_num=Count('id')
                ).order_by('-id')
                context['page'] = 'book_presentation'
                context['book_presentations'] = book_presentations

            # group
            case 'group':
                group = student_groups.filter(id=group_id).first()
                if group:
                    group_lessons = student_lessons.filter(
                        group_id=group_id).order_by('-id').values('id', 'creator__first_name', 'lesson_number', 'created_at', 'start_time', 'end_time', 'status')
                    context['lessons'] = group_lessons
                    context['group'] = group.name
                    context['page'] = 'group'
        
            # lesson
            case 'lesson':
                lesson = student_lessons.filter(id=lesson_id).first()
                if not lesson:
                    return Http404
                homework = self.get_homework_queryset().filter(student_id=student.id, lesson_id=lesson_id).first()
                if homework:
                    context['homework_items'] = self.get_homework_items_queryset().filter(home_work_id=homework.id).order_by('-id').values('id', 'uploaded_file')
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
                context['can_upload'] = True
                if subject_hometask:
                    if subject_hometask.deadline:
                        context['deadline'] = subject_hometask.deadline.strftime('%Y/%m/%d, %H:%M')
                        if subject_hometask.deadline < utc.localize(datetime.datetime.today()):
                            context['can_upload'] = False
                    subject_hometask_items = self.get_hometask_items_queryset().filter(home_task_id=subject_hometask.id).order_by('-id')
                    context['subject_hometasks'] = subject_hometask_items
            
            # projects
            case 'projects':
                if not group_id:
                    raise Http404
                group = self.get_group_students_queryset().filter(student_id=student.id, group_id=group_id).first()
                if not group:
                    raise Http404
                projects = self.get_student_projects().filter(project_card__student_id=student.id, project_card__group_id=group_id).order_by('-id')
                context['page'] = 'projects'
                context['projects'] = {
                    'projects': projects,
                    'project_card': self.get_student_projects_card_queryset().filter(student_id=student.id).filter(group_id=group_id).first(),
                    'uploaded_qty': len(projects)
                }
        
        return render(request, 'edu/student/dashboard.html', context)
    

    def post(self, request, *args, **kwargs):
        user = self.request.user
        uploaded_files = self.request.FILES.getlist('uploaded_files')
        uploaded_file = self.request.FILES.get('uploaded_file')
        data = self.request.POST
        method = data.get('method')
        lesson_id = data.get('lesson_id')
        file_id = data.get('file_id')
        group_id = data.get('group_id')

        
        match method:
            
            # Upload file "HomeWork"
            case 'homework':
                subject_hometask = self.get_hometask_queryset().filter(lesson_id=lesson_id).first()
                if subject_hometask:
                    if subject_hometask.deadline:
                        if subject_hometask.deadline < utc.localize(datetime.datetime.today()):
                            return HttpResponseRedirect(f'?page=lesson&lesson_id={lesson_id}')
                homework, _ = HomeWork.objects.get_or_create(student_id=user.id, lesson_id=lesson_id)
                for uploaded_file in uploaded_files:
                    item = HomeWorkItem(
                        home_work_id=homework.id,
                        uploaded_file=uploaded_file
                    )
                    item.save()
                return HttpResponseRedirect(f'?page=lesson&lesson_id={lesson_id}')
        
            # Edit File
            case 'edit_homework':
                subject_hometask = self.get_hometask_queryset().filter(lesson_id=lesson_id).first()
                if subject_hometask:
                    if subject_hometask.deadline:
                        if subject_hometask.deadline < utc.localize(datetime.datetime.today()):
                            return HttpResponseRedirect(f'?page=lesson&lesson_id={lesson_id}')
                user_file = self.get_homework_items_queryset().filter(id=file_id, home_work__student_id=user.id).first()
                if user_file:
                    user_file.uploaded_file = uploaded_file
                    user_file.save()
                return HttpResponseRedirect(f'?page=lesson&lesson_id={lesson_id}')
            
            #  Delete File
            case 'delete_homework':
                student_homework = self.get_homework_items_queryset().filter(id=file_id, home_work__student_id=user.id).first()
                if student_homework:
                    student_homework.delete()
                    return HttpResponseRedirect(f'?page=lesson&lesson_id={lesson_id}')
        
            # Add book presentation
            case 'add_book_presentation':
                new_book = self.request.POST.get("book")
                if new_book:
                    book_card, _ = StudentBookPresentationCard.objects.get_or_create(student_id=user.id)
                    StudentBookPresentation.objects.create(
                        book_card_id=book_card.id,
                        book=new_book
                    )
                return HttpResponseRedirect('?page=book_presentation')
            
            # add Project
            case 'add_project':
                group = self.get_group_queryset().filter(id=group_id, group_of_student__student_id=user.id).first()
                if not group:
                    raise Http404
                if uploaded_file:
                    project_card, _ = self.get_student_projects_card_queryset().get_or_create(student_id=user.id, group_id=group_id)
                    self.get_student_projects().create(uploaded_file=uploaded_file, project_card_id=project_card.id)
                return HttpResponseRedirect(f'?page=projects&group_id={group_id}')
            
            # edit Project
            case 'edit_project':
                group = self.get_group_queryset().filter(id=group_id, group_of_student__student_id=user.id).first()
                item_obj = self.get_student_projects().filter(id=file_id, project_card__student_id=user.id).first()
                if not group or not item_obj:
                    raise Http404
                if uploaded_file:
                    item_obj.uploaded_file = uploaded_file
                    item_obj.save()
                return HttpResponseRedirect(f'?page=projects&group_id={group_id}')
            
            # edit Project
            case 'delete_project':
                group = self.get_group_queryset().filter(id=group_id, group_of_student__student_id=user.id).first()
                item_obj = self.get_student_projects().filter(id=file_id, project_card__student_id=user.id).first()
                if not group or not item_obj:
                    raise Http404
                item_obj.delete()
                return HttpResponseRedirect(f'?page=projects&group_id={group_id}')
            
        return HttpResponseRedirect('/')

