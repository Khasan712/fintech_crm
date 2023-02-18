from django.db import models

from apps.commons.models import CustomBaseAbstract, CustomWeekAbstract
from apps.v1.edu.models.courses import Course
from apps.v1.user.models import User, Teacher


class Group(CustomBaseAbstract, CustomWeekAbstract):
    name = models.CharField(max_length=70)
    title = models.CharField(max_length=255, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    from_term = models.DateField()
    to_term = models.DateField()

    class Meta:
        verbose_name = 'Guruh'
        verbose_name_plural = 'Guruhlar'

    def __str__(self):
        return f'{self.id} - {self.name}'
