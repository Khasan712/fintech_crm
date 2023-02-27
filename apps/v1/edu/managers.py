from django.db.models import manager

class SubjectManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_subject_guides=True)

class HomeTaskManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_subject_guides=False)