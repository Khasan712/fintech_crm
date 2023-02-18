
from django.db import models

from apps.commons.models import CustomBaseAbstract, CustomWeekAbstract
from apps.v1.edu.models.groups import Group
from apps.v1.user.models import Student


class Lesson(CustomBaseAbstract):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    theme = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name = 'Dars'
        verbose_name_plural = 'Darslar'

    def __str__(self):
        return f'{self.id} - {self.group.name}'


class Attendance(CustomBaseAbstract):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    is_come = models.BooleanField()
    h_m_percentage = models.FloatField(default=0)

    class Meta:
        verbose_name = 'Davomat'
        verbose_name_plural = 'Davomatlar'

    def __str__(self):
        return f'{self.id} - {self.student.first_name}'
