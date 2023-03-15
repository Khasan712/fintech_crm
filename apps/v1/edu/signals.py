from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from datetime import datetime
from django.db import transaction

from apps.v1.edu.models.exams import Exam, ExamStudentCard
from apps.v1.edu.models.groups import GroupStudent, StudentProjectsCard
from apps.v1.edu.models.lessons import Lesson 
from apps.v1.edu.models.presentations import StudentBookPresentationCard, BookPresentationQty


@receiver(post_save, sender=GroupStudent)
def create_project_tasks_for_student(sender, instance, created, **kwargs):
    if created:
        StudentProjectsCard.objects.get_or_create(
            student_id=instance.student.id,
            group_id=instance.group.id,
            course_projects_qty=instance.group.course.number_projects
        )
        book_qty = BookPresentationQty.objects.last()
        StudentBookPresentationCard.objects.get_or_create(student_id=instance.student.id, total_qty=book_qty.book_qty)


@receiver(post_save, sender=Exam)
def exam_signal(sender, instanse, created, **kwargs):
    if created:
        group_students = GroupStudent.objects.select_related('student', 'group', 'creator', 'updater', 'deleter', 'student_first_lesson')
        with transaction.atomic():
            for group_student in group_students:
                ExamStudentCard.objects.get_or_create(
                    exam_id=instanse.id,
                    student_id=group_student.id
                )
