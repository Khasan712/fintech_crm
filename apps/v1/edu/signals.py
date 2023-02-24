from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from apps.v1.edu.models.lessons import Lesson 
from datetime import datetime 

# @receiver(post_save, sender=Lesson)
# def update_lesson(sender, instance, created, **kwargs):
#     if not created:
#         print(sender.status)
#         if instance.status == 'finished':
#             instance.end_time = datetime.now().time().strftime('%H:%M:%S')
#             print('//////////////////////')
#             instance.save()
  