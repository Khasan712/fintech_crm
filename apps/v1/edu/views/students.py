import pytz
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Sum, Count, Case, When, IntegerField, BigAutoField, Q
from django.views.generic.base import View
from django.http.response import Http404
from django.db.models.functions import Coalesce

from apps.v1.user.permissions import UserAuthenticateRequiredMixin
from apps.v1.edu.models.groups import Group
from apps.v1.edu.forms.students import UploadExamItemStudent
from apps.v1.edu.models.lessons import HomeWork, HomeWorkItem, Lesson
from apps.commons.get_querysets import get_book_presentation_queryset, get_book_presentation_item_queryset, \
    get_homework_queryset, get_hometask_items_queryset, get_exam_queryset, get_exam_file_queryset, \
    get_hometask_queryset, get_homework_items_queryset, get_student_projects_card_queryset, get_group_queryset, \
    get_student_projects, get_student_exam_card_queryset, get_student_exam_item_queryset, get_student_in_group_queryset
from apps.v1.edu.models.presentations import StudentBookPresentation, StudentBookPresentationCard
utc=pytz.UTC


class StudentDashboardView(UserAuthenticateRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        page = self.request.GET.get('page')
        group_id = self.request.GET.get('group_id')
        lesson_id = self.request.GET.get('lesson_id')
        exam_id = self.request.GET.get('exam_id')

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
                    "book_presentation": get_book_presentation_queryset(self).filter(student_id=student.id).first(),
                    "book_presentation_qty": len(get_book_presentation_item_queryset(self).filter(book_card__student_id=student.id, is_aproved=True)),
                    "projects": get_student_projects_card_queryset(self).filter(student_id=student.id).annotate(
                        accepted_proj_qty=Coalesce(Count(Case(When(
                            student_project_item__status='accepted',
                            then='student_project_item'
                        ), distinct=True)), 0)
                    )
                }

            # book presentation
            case 'book_presentation':
                book_presentations = get_book_presentation_item_queryset(self).filter(book_card__student_id=student.id).annotate(
                    order_num=Count('id')
                ).order_by('-id')
                context['page'] = 'book_presentation'
                context['book_presentations'] = book_presentations

            # group
            case 'group':
                group = student_groups.filter(id=group_id).values('id', 'name').first()
                if group:
                    group_lessons = student_lessons.filter(
                        group_id=group_id).order_by('-id').values('id', 'creator__first_name', 'lesson_number', 'created_at', 'start_time', 'end_time', 'status')
                    context['lessons'] = group_lessons
                    context['group'] = group
                    context['page'] = 'group'

            # lesson
            case 'lesson':
                lesson = student_lessons.filter(id=lesson_id).first()
                if not lesson:
                    raise Http404
                homework = get_homework_queryset(self).filter(student_id=student.id, lesson_id=lesson_id).first()
                if homework:
                    context['homework_items'] = get_homework_items_queryset(self).filter(home_work_id=homework.id).order_by('-id').values('id', 'uploaded_file')
                context['lesson'] = lesson
                context['page'] = 'lesson'
                subject_guide = get_hometask_queryset(self).filter(
                    lesson_id=lesson_id, is_subject_guides=True
                ).first()
                subject_hometask = get_hometask_queryset(self).filter(
                    lesson_id=lesson_id, is_subject_guides=False
                ).first()
                if subject_guide:
                    subject_guide_items = get_hometask_items_queryset(self).filter(home_task_id=subject_guide.id).order_by('-id')
                    context['subject_guides'] = subject_guide_items
                context['can_upload'] = True
                if subject_hometask:
                    if subject_hometask.deadline:
                        context['deadline'] = subject_hometask.deadline.strftime('%Y/%m/%d, %H:%M')
                        if subject_hometask.deadline < utc.localize(datetime.datetime.today()):
                            context['can_upload'] = False
                    subject_hometask_items = get_hometask_items_queryset(self).filter(home_task_id=subject_hometask.id).order_by('-id')
                    context['subject_hometasks'] = subject_hometask_items
            
            # projects
            case 'projects':
                if not group_id:
                    raise Http404
                group = get_student_in_group_queryset(self).filter(student_id=student.id, group_id=group_id).first()
                if not group:
                    raise Http404
                projects = get_student_projects().filter(project_card__student_id=student.id, project_card__group_id=group_id).order_by('-id')
                context['page'] = 'projects'
                context['projects'] = {
                    'projects': projects,
                    'project_card': get_student_projects_card_queryset(self).filter(student_id=student.id).filter(group_id=group_id).first(),
                    'uploaded_qty': projects.aggregate(qty=Coalesce(Count('id'), 0))['qty'],
                    'accepted_qty': projects.filter(status='accepted').aggregate(qty=Coalesce(Count('id'), 0))['qty'],
                    'rejected_qty': projects.filter(status='rejected').aggregate(qty=Coalesce(Count('id'), 0))['qty'],
                    'in_progress_qty': projects.filter(status='in_progress').aggregate(qty=Coalesce(Count('id'), 0))['qty'],
                }
        
            # exams
            case 'exams':
                group = get_group_queryset(self).filter(id=group_id, group_of_student__student_id=student.id).values('id', 'name').first()
                if not group:
                    raise Http404
                context['page'] = 'exams'
                context['exams'] = get_exam_queryset(self).filter(group_id=group_id, exam_item__student_id=student.id,).annotate(
                    uploaded_qty=Coalesce(Count('exam_item__student_item_exam_card'), 0, output_field=IntegerField()),
                    in_progress_qty=Coalesce(Count(Case(When(
                        exam_item__student_item_exam_card__status='in_progress',
                        then='exam_item__student_item_exam_card'
                    ))), 0, output_field=IntegerField()),
                    accepted_qty=Coalesce(Count(Case(When(
                        exam_item__student_item_exam_card__status='accepted',
                        then='exam_item__student_item_exam_card'
                    ))), 0, output_field=IntegerField()),
                ).values('id', 'name', 'deadline', 'created_at', 'uploaded_qty', 'in_progress_qty', 'accepted_qty')
                context['group'] = group

            # exam
            case 'exam':
                exam = get_exam_queryset(self).filter(
                    id=exam_id, group_id=group_id, group__group_of_student__student_id=student.id,
                    exam_item__student_id=student.id
                ).first()
                if not exam:
                    raise Http404
                context['page'] = 'exam'
                context['exam'] = exam
                context['group'] = get_group_queryset(self).filter(id=group_id).values('id', 'name', 'teacher').first()
                context['exam_items'] = get_exam_file_queryset(self).filter(exam=exam_id)
                context['my_items'] = get_student_exam_item_queryset(self).filter(exam_card__exam_id=exam_id, exam_card__student_id=student.id).values(
                    'id', 'uploaded_file', 'netlify_link', 'status', 'name', 'github_link', 'created_at'
                ).order_by('-id')
                context['exam_card'] = get_student_exam_card_queryset(self).filter(exam_id=exam_id, student_id=student.id).annotate(
                    uploaded_files_qty=Coalesce(Count(
                        'student_item_exam_card', distinct=True
                    ), 0, output_field=IntegerField()),
                    accepted_files_qty=Coalesce(Count(Case(When(
                            student_item_exam_card__status='accepted',
                            then='student_item_exam_card'
                    )), distinct=True), 0, output_field=IntegerField()),
                    in_progress_files_qty=Coalesce(Count(Case(When(
                            student_item_exam_card__status='in_progress',
                            then='student_item_exam_card'
                    )), distinct=True), 0, output_field=IntegerField()),
                    rejected_files_qty=Coalesce(Count(Case(When(
                            student_item_exam_card__status='rejected',
                            then='student_item_exam_card'
                    )), distinct=True), 0, output_field=IntegerField())
                ).values('id', 'uploaded_files_qty', 'accepted_files_qty', 'in_progress_files_qty', 'rejected_files_qty').first()
                context['can_upload'] = False if exam.deadline < utc.localize(datetime.datetime.today()) else True
                
        return render(request, 'edu/student/dashboard.html', context)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.POST
        data_media = self.request.FILES
        uploaded_files = data_media.getlist('uploaded_files')
        uploaded_file = data_media.get('uploaded_file')
        method = data.get('method')
        lesson_id = data.get('lesson_id')
        file_id = data.get('file_id')
        group_id = data.get('group_id')
        exam_id = data.get('exam_id')
        item_id = data.get('item_id')
        
        match method:
            
            # Upload file "HomeWork"
            case 'homework':
                subject_hometask = get_hometask_queryset(self).filter(lesson_id=lesson_id).first()
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
                subject_hometask = get_hometask_queryset(self).filter(lesson_id=lesson_id).first()
                if subject_hometask:
                    if subject_hometask.deadline:
                        if subject_hometask.deadline < utc.localize(datetime.datetime.today()):
                            return HttpResponseRedirect(f'?page=lesson&lesson_id={lesson_id}')
                user_file = get_homework_items_queryset(self).filter(id=file_id, home_work__student_id=user.id).first()
                if user_file:
                    user_file.uploaded_file = uploaded_file
                    user_file.save()
                return HttpResponseRedirect(f'?page=lesson&lesson_id={lesson_id}')
            
            #  Delete File
            case 'delete_homework':
                student_homework = get_homework_items_queryset(self).filter(id=file_id, home_work__student_id=user.id).first()
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
                group = get_group_queryset(self).filter(id=group_id, group_of_student__student_id=user.id).first()
                if not group:
                    raise Http404
                if uploaded_file:
                    project_card, _ = get_student_projects_card_queryset(self).get_or_create(student_id=user.id, group_id=group_id)
                    get_student_projects().create(
                        uploaded_file=uploaded_file, project_card_id=project_card.id, name=request.POST['name'],
                        github_link=request.POST['github_link'], netlify_link=request.POST.get('netlify_link')
                    )
                return HttpResponseRedirect(f'?page=projects&group_id={group_id}')
            
            # edit Project
            case 'edit_project':
                group = get_group_queryset(self).filter(id=group_id, group_of_student__student_id=user.id).first()
                item_obj = get_student_projects().filter(id=file_id, project_card__student_id=user.id).first()
                if not group or not item_obj:
                    raise Http404
                if uploaded_file:
                    item_obj.uploaded_file = uploaded_file
                    item_obj.save()
                return HttpResponseRedirect(f'?page=projects&group_id={group_id}')
            
            # edit Project
            case 'delete_project':
                group = get_group_queryset(self).filter(id=group_id, group_of_student__student_id=user.id).first()
                item_obj = get_student_projects().filter(id=file_id, project_card__student_id=user.id).first()
                if not group or not item_obj:
                    raise Http404
                item_obj.delete()
                return HttpResponseRedirect(f'?page=projects&group_id={group_id}')
            
            # Exam upload
            case 'exam_upload':
                exam_card = get_student_exam_card_queryset(self).filter(exam_id=exam_id, student_id=user.id).first()
                if not exam_card:
                    raise Http404
                exam_upload_form = UploadExamItemStudent(data or None, data_media or None)
                if exam_upload_form.is_valid():
                    obj = exam_upload_form.save(commit=True)
                    obj.exam_card = exam_card
                    obj.save()
                return HttpResponseRedirect(f'?page=exam&exam_id={exam_id}&group_id={exam_card.exam.group.id}')
            
            # Exam edit
            case 'exam_edit_item':
                exam_item = get_student_exam_item_queryset(self).filter(id=item_id, exam_card__exam_id=exam_id, exam_card__student_id=user.id).first()
                if not exam_item:
                    raise Http404
                exam_item_edit_form = UploadExamItemStudent(data or None, data_media or None, instance=exam_item)
                if exam_item_edit_form.is_valid():
                    exam_item_edit_form.save()
                return HttpResponseRedirect(f'?page=exam&exam_id={exam_id}&group_id={exam_item.exam_card.exam.group.id}')
            
            # Exam delete
            case 'exam_edit_delete':
                exam_item = get_student_exam_item_queryset(self).filter(id=item_id, exam_card__exam_id=exam_id, exam_card__student_id=user.id).first()
                group_id = exam_item.exam_card.exam.group.id
                if not exam_item:
                    raise Http404
                exam_item.delete()
                return HttpResponseRedirect(f'?page=exam&exam_id={exam_id}&group_id={group_id}')
            
        return HttpResponseRedirect('/')

