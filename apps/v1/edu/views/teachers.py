import datetime as dt
from datetime import datetime
from django.shortcuts import render
from django.views.generic.base import View

from django.http.response import Http404, HttpResponse, HttpResponseRedirect

from django.db import transaction
from django.db.models import Count, Sum, Q, When, F, Case
from django.db.models.functions import Coalesce

from apps.v1.edu.forms import teachers
from apps.v1.edu.models.exams import ExamFile
from apps.v1.user.permissions import UserAuthenticateRequiredMixin
from apps.v1.edu.models.lessons import Attendance, HomeTask, HomeTaskItem
from apps.commons.get_querysets import get_hometask_queryset, get_homework_items_queryset, \
    get_student_projects_card_queryset, get_students_queryset, get_student_exam_card_queryset, get_attendance_queryset,\
    get_hometask_items_queryset, get_student_projects, get_group_queryset, get_lessons_queryset, \
    get_student_in_group_queryset, get_exam_queryset, get_exam_file_queryset, get_student_exam_item_queryset


class TeacherDashboardView(UserAuthenticateRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        teacher = request.user
        page = self.request.GET.get('page')
        group_id = self.request.GET.get('group_id')
        lesson_id = self.request.GET.get('lesson_id')
        student_id = self.request.GET.get('student_id')
        exam_id = self.request.GET.get('exam_id')

        teacher_groups = get_group_queryset(self).filter(teacher_id=teacher.id)
        teacher_lessons = get_lessons_queryset(self)
        context = {
            'user': teacher,
            'page': 'dashboard',
            'groups': teacher_groups.values('id', 'name').order_by('-id')
        }

        match page:

            # Dashboard
            case None | 'dashboard':
                group_statistics = teacher_groups.annotate(students_qty=Count('group_of_student__student'))
                context['dashboard_statistics'] = {
                    "group_statistics": group_statistics
                }

            # Group page
            case 'group':
                group = teacher_groups.filter(id=group_id).first()
                if not group:
                    raise Http404
                group_lessons = teacher_lessons.filter(group_id=group_id).order_by('-id').values(
                    'id', 'creator__first_name', 'lesson_number', 'created_at', 'start_time', 'end_time', 'status'
                )
                context['lessons'] = group_lessons
                context['group'] = {
                    'id': group.id,
                    'name': group.name
                }
                context['page'] = 'group'

            # Lesson page
            case 'lesson':
                lesson = teacher_lessons.filter(id=lesson_id).first()
                if not lesson:
                    raise Http404
                subject_guide = get_hometask_queryset(self).filter(
                    lesson_id=lesson_id, is_subject_guides=True
                ).first()
                subject_hometask = get_hometask_queryset(self).filter(
                    lesson_id=lesson_id, is_subject_guides=False
                ).first()
                if subject_guide:
                    subject_guide_items = get_hometask_items_queryset(self).filter(home_task_id=subject_guide.id).order_by('-id')
                    context['subject_guides'] = subject_guide_items
                if subject_hometask:
                    subject_hometask_items = get_hometask_items_queryset(self).filter(home_task_id=subject_hometask.id).order_by('-id')
                    context['subject_hometasks'] = subject_hometask_items
                context['lesson'] = lesson
                context['page'] = 'lesson'
                context['students'] = get_attendance_queryset(self).filter(lesson_id=lesson.id, lesson__creator_id=teacher.id).annotate(
                    student_type=Q(Case(When(student__student_in_group__group_id=lesson.group.id, then='student__student_in_group__student_type')))
                ).values(
                    'student__id', 'student__first_name', 'student__last_name', 'is_come', 'h_m_percentage'
                )

            # Students page
            case 'group_students':
                group = get_group_queryset(self).filter(id=group_id, teacher_id=teacher.id).first()
                if not group:
                    raise Http404
                group_students = get_student_in_group_queryset(self).filter(group_id=group_id)
                context['group'] = {
                    'id':group_id,
                    'name': group.name
                },
                context['group'] = context['group'][0]
                context['page'] = 'group_students'
                context['students'] = group_students.annotate(
                    uploaded_file_qty=Coalesce(Count(Case(When(
                        student__student_projects_card__group_id=group_id,
                        then='student__student_projects_card__student_project_item'
                    )),distinct=True), 0),
                    weekly_point=Coalesce(Sum(Case(When(
                        student__student_attendance__lesson__group_id=group_id,
                        student__student_attendance__created_at__gte=(dt.date.today() - dt.timedelta(days=dt.date.today().weekday())),
                        student__student_attendance__created_at__lte=datetime.now(),
                        then='student__student_attendance__h_m_percentage',
                    )), distinct=True), 0),
                    accepted_project_qty=Coalesce(Count(Case(When(
                        student__student_projects_card__group_id=group_id,
                        student__student_projects_card__student_project_item__status='accepted',
                        then='student__student_projects_card__student_project_item'
                    )), distinct=True), 0),
                )
        
            # Student in lesson
            case 'student_in_lesson':
                student = get_students_queryset(self).filter(student_attendance__student_id=student_id).first()
                if not student:
                    raise Http404
                context['page'] = 'student_in_lesson'
                context['student'] = student
                context['homework_items'] = get_homework_items_queryset(self).filter(home_work__student_id=student_id, home_work__lesson_id=lesson_id)
        
            # Student projects page
            case 'student_projects':
                group = get_group_queryset(self).filter(id=group_id).first()
                student = get_students_queryset(self).filter(id=student_id, student_in_group__group_id=group.id).first()
                if not group or not student:
                    raise Http404
                context['page'] = 'student_projects'
                context['group_id'] = group_id
                context['student'] = {
                    'id': student.id,
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                }
                context['projects'] = get_student_projects().filter(project_card__student_id=student_id, project_card__group_id=group_id)
                context['projects_statistics'] = get_student_projects_card_queryset(self).filter(student_id=student_id, group_id=group_id).annotate(
                    uploaded_proj_qty=Coalesce(Count('student_project_item', distinct=True), 0),
                    accepted_proj_qty=Coalesce(Count(Case(When(
                        student_project_item__status='accepted',
                        then='student_project_item'
                    )), distinct=True), 0),
                    rejected_proj_qty=Coalesce(Count(Case(When(
                        student_project_item__status='rejected',
                        then='student_project_item'
                    )), distinct=True), 0),
                    in_progress_proj_qty=Coalesce(Count(Case(When(
                        student_project_item__status='in_progress',
                        then='student_project_item'
                    )), distinct=True), 0),
                ).first()
            
            # Exams page
            case 'exams':
                group = get_group_queryset(self).filter(id=group_id).first()
                if not group:
                    raise Http404
                group_exams = get_exam_queryset(self).filter(group_id=group_id).annotate(
                    students_qty=Coalesce(Count(Case(When(
                        group__group_of_student__group_id=group_id,
                        then='group__group_of_student'
                    )), distinct=True), 0)
                ).order_by('-id')
                context['page'] = 'exams'
                context['exams'] = group_exams
                context['group'] = group
        
            # Exam page
            case 'exam':
                exam = get_exam_queryset(self).filter(id=exam_id, group_id=group_id).first()
                if exam:
                    context['page'] = 'exam'
                    context['exam'] = exam
                    context['group_id'] = group_id
                    context['exam_items'] = get_exam_file_queryset(self).filter(exam_id=exam_id).order_by('-id')
                    context['students'] = get_students_queryset(self).filter(
                        student_exam_card__isnull=False, student_exam_card__exam__group_id=group_id
                    ).annotate(
                        uploaded_files_qty=Coalesce(Count(Case(When(
                            student_exam_card__exam_id=exam_id,
                            then='student_exam_card__student_item_exam_card'
                        )), distinct=True), 0),
                        accepted_files_qty=Coalesce(Count(Case(When(
                            student_exam_card__exam_id=exam_id,
                            student_exam_card__student_item_exam_card__status='accepted',
                            then='student_exam_card__student_item_exam_card'
                        )), distinct=True), 0)
                    ).values('id', 'first_name', 'last_name', 'student_type', 'uploaded_files_qty', 'accepted_files_qty')

            # Student in exam page
            case 'student_in_exam':
                exam = get_exam_queryset(self).filter(id=exam_id).first()
                student_group = get_student_in_group_queryset(self).filter(student_id=student_id, student__student_exam_card__exam__group_id=exam.group.id).first()
                if student_group:
                    context['page'] = 'student_in_exam'
                    context['uploaded_files'] = get_student_exam_item_queryset(self).filter(
                        exam_card__student_id=student_id, exam_card__exam_id=exam_id
                    ).order_by('-id')
                    context['student'] = {
                        'id': student_group.student.id,
                        'first_name': student_group.student.first_name,
                        'last_name': student_group.student.last_name,
                    }
                    context['exam_card'] = get_student_exam_card_queryset(self).filter(exam_id=exam_id, student_id=student_id).annotate(
                        uploaded_files_qty=Coalesce(Count('student_item_exam_card', distinct=True), 0),
                        accepted_files_qty=Coalesce(Count(Case(When(
                            student_item_exam_card__status='accepted',
                            then='student_item_exam_card'
                        )), distinct=True), 0),
                        in_progress_files_qty=Coalesce(Count(Case(When(
                            student_item_exam_card__status='in_progress',
                            then='student_item_exam_card'
                        )), distinct=True), 0),
                        rejected_files_qty=Coalesce(Count(Case(When(
                            student_item_exam_card__status='rejected',
                            then='student_item_exam_card'
                        )), distinct=True), 0)
                    ).first()

        return render(request, 'edu/teacher/dashboard.html', context)

    def post(self, request, *args, **kwargs):
        creator = self.request.user
        data = self.request.POST
        data_media = self.request.FILES
        method = data.get('method')
        page = data.get('page')
        group_id = data.get('group_id')
        student_id = data.get('student_id')
        lesson_id = data.get('lesson_id')
        lesson_status = data.get('status')
        item_id = data.get('item_id')
        exam_id = data.get('exam_id')
        uploaded_file = data_media.get('uploaded_file')
        uploaded_files = data_media.getlist('uploaded_files')
        
        parametr = '/'

        match method:
            
            # Add lesson
            case 'create_lesson':
                group = get_group_queryset(self).filter(id=group_id, teacher_id=creator.id).first()
                if group:
                    create_lesson_form = teachers.CreateLessonForm(self.request.POST)
                    if not create_lesson_form.is_valid():
                        raise Http404
                    lesson_commit = create_lesson_form.save(commit=False)
                    lesson_commit.creator_id = creator.id
                    lesson_commit.group_id = group_id
                    lesson_commit.lesson_number = get_lessons_queryset(self).filter(group_id=group_id).count() + 1
                    lesson_commit.save()
                    group_students = get_student_in_group_queryset(self).filter(group_id=group.id)
                    for g_student in group_students:
                        Attendance.objects.get_or_create(student_id=g_student.student.id, lesson_id=lesson_commit.id)
                        if not g_student.student_first_lesson:
                            g_student.student_first_lesson_id = lesson_commit.id
                            g_student.save()
                    parametr = f'?page=group&group_id={group_id}'
            
            # Edit lesson
            case 'update_lesson':
                lesson = get_lessons_queryset(self).filter(id=lesson_id, creator_id=creator.id).first()
                if lesson:
                    if lesson.status == 'started' and lesson_status == 'finished':
                        update_lesson_form = teachers.UpdateLessonForm(data or None, instance=lesson)
                        if not update_lesson_form.is_valid():
                            return HttpResponse(update_lesson_form.errors)
                        update_lesson_commit = update_lesson_form.save(commit=True)
                        update_lesson_commit.end_time = datetime.now().time().strftime('%H:%M:%S')
                        update_lesson_commit.save()
                    else:
                        update_lesson_form = teachers.UpdateLessonForm(data or None, instance=lesson)
                        if not update_lesson_form.is_valid():
                            return HttpResponse(update_lesson_form.errors)
                        update_lesson_form.save()
                    parametr = f'?page=lesson&lesson_id={lesson_id}'

            # Create attendency
            case 'create_attendency':
                students_id = data.getlist('students_id')
                studnets_iscome = data.getlist('iscome')
                students_h_w_percentage = data.getlist('h_w_percentage')
                lesson = get_lessons_queryset(self).filter(id=lesson_id).first()
                if lesson.status == 'started':
                    for student in range(len(students_id)):
                        student_attend_obj = get_attendance_queryset(self).filter(
                            student_id=int(students_id[student]), lesson_id=lesson_id
                        ).first()
                        if student_attend_obj:
                            if student_attend_obj.is_come != bool(studnets_iscome[student] == 'True'):
                                student_attend_obj.is_come = bool(studnets_iscome[student] == 'True')
                                student_attend_obj.save()
                            if student_attend_obj.h_m_percentage != int(students_h_w_percentage[student]):
                                student_attend_obj.h_m_percentage = int(students_h_w_percentage[student])
                                student_attend_obj.save()
                parametr = f'?page=lesson&lesson_id={lesson_id}'

            # Add subject guides
            case 'subject_guides':
                if page == 'lesson':
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
                                    HomeTaskItem.objects.create(home_task_id=subject_hometask.id, uploaded_file=uploaded_file)
                parametr = f'?page=lesson&lesson_id={lesson_id}'
                    
            # Edit subject guide or home task
            case "edit_guides_and_tasks":
                text = data.get('text')
                uploaded_file = self.request.FILES.get('uploaded_file')
                hometask_item = get_hometask_items_queryset(self).filter(
                    id=item_id, home_task__lesson_id=lesson_id
                ).first()
                if hometask_item:
                    if text and text != hometask_item.text:
                        hometask_item.text = text
                    elif uploaded_file:
                        hometask_item.uploaded_file = uploaded_file
                    hometask_item.save()
                parametr = f'?page=lesson&lesson_id={lesson_id}'
                
            # Delete subject guide or home task
            case "delete_guides_and_tasks":
                hometask_item = get_hometask_items_queryset(self).filter(
                    id=item_id, home_task__lesson_id=lesson_id
                ).first()
                if hometask_item:
                    hometask_item.delete()
                parametr = f'?page=lesson&lesson_id={lesson_id}'
        
            # Give status to student proj
            case 'give_status_to_proj':
                group = get_group_queryset(self).filter(id=group_id, teacher_id=creator.id).first()
                student = get_student_in_group_queryset(self).filter(group_id=group_id, student_id=student_id).first()
                if not group or not student:
                    raise Http404
                items_id = data.getlist('item_id')
                items_status = data.getlist('status')
                with transaction.atomic():
                    for i in range(len(items_id)):
                        student_proj = get_student_projects().filter(id=items_id[i], project_card__student_id=student_id).first()
                        if not student_proj:
                            raise Http404
                        if student_proj.status != items_status[i]:
                            student_proj.status = items_status[i]
                            student_proj.save()
                parametr = f'?page=student_projects&group_id={group_id}&student_id={student_id}'
        
            # Edit exam
            case 'edit_exam':
                exam = get_exam_queryset(self).filter(id=exam_id, group_id=group_id, group__teacher_id=creator.id).first()
                if exam:
                    exam_form = teachers.ExamForm(self.request.POST, instance=exam)
                    if not exam_form.is_valid():
                        raise Http404
                    exam_form.save()
                    parametr = f'?page=exam&exam_id={exam_id}&group_id={group_id}'
            
            # Add exam
            case 'add_exam':
                group = get_group_queryset(self).filter(id=group_id, teacher_id=creator.id).first()
                if not group:
                    raise Http404
                add_exam_form = teachers.ExamForm(self.request.POST)
                if add_exam_form.is_valid():
                    obj = add_exam_form.save(commit=True)
                    obj.group = group
                    obj.save()
                parametr = f'?page=exams&&group_id={group_id}'
                
            # Delete exam
            case 'delete_exam':
                exam = get_exam_queryset(self).filter(id=exam_id, group__teacher_id=creator.id).first()
                if not exam:
                    raise Http404
                exam.delete()
                parametr = f'?page=exams&group_id={group_id}'

            # Check the exam
            case 'check_exam':
                status = data.getlist('status')
                item_id = data.getlist('item_id')
                with transaction.atomic():
                    for i in range(len(item_id)):
                        item_obj = get_student_exam_item_queryset(self).filter(
                            exam_card__student_id=student_id, exam_card__exam_id=exam_id, id=item_id[i]
                        ).first()
                        if not item_obj:
                            raise Http404
                        if item_obj.status != status[i]:
                            item_obj.status = status[i]
                            item_obj.save()
                parametr = f'?page=student_in_exam&exam_id={exam_id}&student_id={student_id}'
        
            # Upload exam files
            case 'upload_exam_files':
                name = data.get("name")
                exam = get_exam_queryset(self).filter(id=exam_id, group__teacher_id=creator.id).first()
                group = get_group_queryset(self).filter(id=group_id, teacher_id=creator.id).first()
                if not exam or not name or not group:
                    raise Http404
                url_address = data.get("url_address")
                if uploaded_files:
                    with transaction.atomic():
                        for uploaded_file in uploaded_files:
                            exam_item_obj = ExamFile(exam_id=exam_id, name=name)
                            exam_item_obj.uploaded_file=uploaded_file
                            if url_address:
                                exam_item_obj.url_address=url_address
                            exam_item_obj.save()
                else:
                    exam_item_obj = ExamFile(exam_id=exam_id, name=name)
                    exam_item_obj.url_address=url_address
                    exam_item_obj.save()
                parametr = f'?page=exam&exam_id={exam_id}&group_id={group_id}'
                
            # Edit exam file
            case 'edit_exam_item':
                exam = get_exam_queryset(self).filter(id=exam_id, group__teacher_id=creator.id).first()
                group = get_group_queryset(self).filter(id=group_id, teacher_id=creator.id).first()
                item = get_exam_file_queryset(self).filter(id=item_id, exam_id=exam_id).first()
                if not exam or not group or not item:
                    raise Http404
                edit_exam_form = teachers.ExamFileForms(data or None, data_media or None, instance=item)
                if edit_exam_form.is_valid():
                    edit_exam_form.save()
                else:
                    edit_exam_form
                parametr = f'?page=exam&exam_id={exam_id}&group_id={group_id}'
                
            # Delete exam file or item
            case 'delete_exam_item':
                exam = get_exam_queryset(self).filter(id=exam_id, group__teacher_id=creator.id).first()
                group = get_group_queryset(self).filter(id=group_id, teacher_id=creator.id).first()
                item = get_exam_file_queryset(self).filter(id=item_id, exam_id=exam_id).first()
                if not exam or not group or not item:
                    raise Http404
                item.delete()
                parametr = f'?page=exam&exam_id={exam_id}&group_id={group_id}'
                         
        return HttpResponseRedirect(parametr)
