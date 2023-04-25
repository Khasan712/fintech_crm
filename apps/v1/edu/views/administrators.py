import datetime as dT
import calendar as cL
from datetime import datetime
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import (
    Count,
    Sum,
    IntegerField,
    Case,
    When,
    Q,
    Value,
    Prefetch,
    Subquery,
    OuterRef
)
from django.http.response import Http404
from django.views.generic.base import View
from django.db.models.functions import Coalesce, Concat


from apps.commons.get_pages import get_administrator_render
from apps.v1.user.permissions import UserAuthenticateRequiredMixin
from apps.v1.edu.models.groups import GroupStudent
from apps.v1.edu.forms.administrators_forms import GroupAddForm
from apps.commons.get_querysets import (
    get_students_queryset,
    get_group_queryset,
    get_course_queryset,
    get_teacher_queryset,
    get_attendance_queryset,
    get_rent_books_queryset,
    get_lessons_queryset
)



class AdministratorDashboardView(UserAuthenticateRequiredMixin, View):

    def get_filtered_group(self):
        data = self.request.GET
        teacher_id = data.get("teacher_id")
        course = data.get("course")
        queryset = get_group_queryset(self)
        if not teacher_id == 'all' and teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        if not course == 'all' and course:
            queryset = queryset.filter(group_type=course)
        return queryset

    def get(self, request, *args, **kwargs):
        administrator = self.request.user
        data = self.request.GET
        page = data.get('page')
        group_id = data.get('group_id')
        teacher_id = data.get('teacher_id')

        context = {
            "user": administrator,
            'page': "dashboard"
        }

        match page:
            
            # Dashboard
            case None | 'dashboard':
                students = get_students_queryset(self)
                courses = get_course_queryset(self)
                context.update(
                    {   
                        "students": students.aggregate(
                            total_qty=Coalesce(Count('id', distinct=True), 0, output_field=IntegerField()),
                            not_verefied_qty=Coalesce(Count(Case(When(is_verified=False, then='id')), distinct=True), 0, output_field=IntegerField()),
                            studied_qty=Coalesce(Count(Case(When(is_verified=True, student_in_group__student_status="studying", then='id')), distinct=True), 0, output_field=IntegerField()),
                            graduated_qty=Coalesce(Count(Case(When(student_in_group__student_status='finished', then='student_in_group')), distinct=True), 0, output_field=IntegerField()),
                            
                            gone_qty=Coalesce(Count(Case(When(is_gone=True, then='id')), distinct=True), 0, output_field=IntegerField()),
                            online_qty=Coalesce(Count(Case(When(student_in_group__student_type='online', student_in_group__student_status='studying', then='student_in_group')), distinct=True), 0, output_field=IntegerField()),
                            offline_qty=Coalesce(Count(Case(When(student_in_group__student_type='offline', student_in_group__student_status='studying', then='student_in_group')), distinct=True), 0, output_field=IntegerField()),

                        ),
                        'courses': courses.annotate(
                            groups_qty=Coalesce(Count(Case(When(group_course__group_status='active', then='group_course')), distinct=True), 0, output_field=IntegerField()),
                            students_qty=Coalesce(Count(Case(When(group_course__group_of_student__student_status='studying', then='group_course__group_of_student')), distinct=True), 0, output_field=IntegerField())
                        ),
                    }
                )
                return get_administrator_render(request, context)
            
            # Groups
            case 'groups':
                context.update({
                    'page': 'groups',
                    'courses': get_course_queryset(self).values('id', 'name'),
                    'teachers': get_teacher_queryset(self).values('id', 'first_name'),
                    'groups': self.get_filtered_group().filter(group_status='active').annotate(
                        students_qty=Coalesce(Count('group_of_student', distinct=True), 0, output_field=IntegerField()),
                    ).order_by('-id')
                })
                return get_administrator_render(request, context)

            # Lessons
            case 'lessons':
                context.update({
                    'page': 'lessons',
                    'group_id': group_id,
                    'lessons': get_lessons_queryset(self).filter(group_id=group_id, group__teacher_id=teacher_id).annotate(
                        came_qty=Coalesce(Count(Case(When(lesson_attendancy__is_come=True, then='lesson_attendancy')), distinct=True), 0, output_field=IntegerField()),
                        not_came_qty=Coalesce(Count(Case(When(lesson_attendancy__is_come=False, then='lesson_attendancy')), distinct=True), 0, output_field=IntegerField()),
                    ).order_by('-id')
                })
                return get_administrator_render(request, context)

                
            # Group attendancy
            case 'group_attendancy':

                """ This code is CHAT-GPT answer """
                current_day = dT.date.today()
                days_in_month = cL.monthrange(current_day.year, current_day.month)[1]
                group = get_group_queryset(self).filter(id=group_id).first()
                if not group:
                    raise Http404
                all_students = get_students_queryset(self)
                group_students = all_students.filter(
                    student_in_group__group_id=group_id,
                )
                group_attendance = get_attendance_queryset(self).filter(
                    lesson__group_id=group_id,
                    created_at__range=(current_day.replace(day=1), current_day.replace(day=days_in_month))
                )
                students = []
                for n, student in enumerate(group_students, start=1):
                    s_data = {'order': n, 'student': student}
                    attendance_records = [0] * days_in_month
                    for att in group_attendance:
                        if att.student.id == student.id:
                            attendance_records[att.created_at.day - 1] = 1 if att.is_come else 2
                    s_data['atts'] = attendance_records
                    students.append(s_data)
                
                
                context.update({
                    'page': 'group_attendancy',
                    'days': range(1, days_in_month+1),
                    'students': students[::-1],
                    'all_students': all_students.filter(~Q(student_in_group__group_id=group_id)).values('id', 'first_name', 'phone_number'),
                    'group_id': group_id,
                })
                return get_administrator_render(request, context)
        

            # Students
            case 'students':
                context.update({
                    'page': 'students',
                    'students': get_students_queryset(self).values('id', 'first_name', 'last_name', 'phone_number', 'is_verified').order_by('-id')
                })
                return get_administrator_render(request, context)
            
            
            # Teachers
            case 'teachers':
                context.update({
                    'page': 'teachers',
                    'teachers': get_teacher_queryset(self).annotate(
                        groups_qty=Coalesce(Count((Case(When(group_teacher__group_status='active', then='group_teacher'))), distinct=True), 0, output_field=IntegerField()),
                        students_qty=Coalesce(Count(Case(When(
                            group_teacher__group_of_student__student_status='studying',
                            then='group_teacher__group_of_student'
                        )), distinct=True), 0, output_field=IntegerField())
                    ).values('id', 'first_name', 'last_name', 'phone_number', 'groups_qty', 'students_qty')
                })
                return get_administrator_render(request, context)
            
            # Books
            case 'books':
                context.update({
                    'page': 'books',
                    'rent_books': get_rent_books_queryset(self)
                })
                return get_administrator_render(request, context)

        return get_administrator_render(request, context)


    def post(self, request, *args, **kwargs):
        user = request.user
        request_post_data = self.request.POST
        method = request_post_data.get("method")
        group_id = request_post_data.get("group_id")
        online_students_ids = request_post_data.getlist('online_students_ids')
        offline_students_ids = request_post_data.getlist('offline_students_ids')
        
        match method:
            
            # Add group
            case 'add.group':
                """
                    Create group,
                    params => method=add.group
                    {
                        'group fields',
                        online_students_ids: [...],
                        offline_students_ids: [...]
                    }
                """
                group_add_form = GroupAddForm(request_post_data)
                if group_add_form.is_valid():
                    obj = group_add_form.save(commit=False)
                    obj.creator = user
                    obj.save()
                group_students = []
                for students_id, student_type in ((online_students_ids, 'online'), (offline_students_ids, 'offline')):
                    group_students.extend([
                        GroupStudent(
                            student_id=student_id, group_id=obj.id, student_type=student_type, creator_id=user.id
                        )
                        for student_id in students_id
                    ])
                if group_students:
                    GroupStudent.objects.bulk_create(group_students)
                return HttpResponseRedirect(f'?page=groups')


            # Add student on group
            case 'add.student.on.group':
                """
                    {
                        'online_students_ids': [...],
                        'offline_students_ids': [...],
                    }
                """
                group = get_group_queryset(self).filter(id=group_id).first()
                if not group:
                    raise Http404
                group_students = []
                for students_id, student_type in ((online_students_ids, 'online'), (offline_students_ids, 'offline')):
                    group_students.extend([
                        GroupStudent(
                            student_id=student_id, group_id=group_id, student_type=student_type, creator_id=user.id
                        )
                        for student_id in students_id
                    ])
                if group_students:
                    GroupStudent.objects.bulk_create(group_students)
                    
                return HttpResponseRedirect(f'?page=group_attendancy&group_id={group_id}')
            
            # Edit or Delete student from group
            case 'edit.delete.student.from.group':
                # student
                pass
