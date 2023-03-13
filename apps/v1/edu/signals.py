from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from apps.v1.edu.models.lessons import Lesson 
from apps.v1.edu.models.groups import GroupStudent, StudentProjectsCard
from apps.v1.edu.models.presentations import StudentBookPresentationCard, BookPresentationQty
from datetime import datetime 

# @receiver(post_save, sender=Lesson)
# def update_lesson(sender, instance, created, **kwargs):
#     if not created:
#         if instance.status == 'finished':
#             instance.end_time = datetime.now().time().strftime('%H:%M:%S')
#             instance.save()


@receiver(post_save, sender=GroupStudent)
def create_project_tasks_for_student(sender, instance, created, **kwargs):
    if created:
        StudentProjectsCard.objects.get_or_create(
            student_id=instance.student.id,
            group_id=instance.group.id,
            course_projects_qty=instance.group.course.number_projects
        )
        book_qty = BookPresentationQty.objects.last()
        StudentBookPresentationCard.objects.get_or_create(stundent_id=instance.student.id, total_qty=book_qty.book_qty)


