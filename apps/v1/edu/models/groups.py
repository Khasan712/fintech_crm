from django.db import models

from apps.commons.models import CustomBaseAbstract, CustomWeekAbstract
from apps.v1.edu.enums import StudentInGroupStatus
from apps.v1.edu.models.courses import Course
from apps.v1.user.models import Student, User, Teacher


class Group(CustomBaseAbstract, CustomWeekAbstract):
    name = models.CharField(max_length=70)
    title = models.CharField(max_length=255, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='group_creator')
    updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='group_updater', blank=True)
    deleter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='group_deleter', blank=True)

    start_time = models.TimeField()
    end_time = models.TimeField()
    from_term = models.DateField()
    to_term = models.DateField()

    class Meta:
        verbose_name = 'Guruh'
        verbose_name_plural = 'Guruhlar'

    def __str__(self):
        return f'{self.id} - {self.name}'


class GroupStudent(CustomBaseAbstract):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='student_in_group')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_of_student')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='group_creator_student')
    updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='group_updater_student', blank=True)
    deleter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='group_deleter_student', blank=True)
    student_status = models.CharField(max_length=8, choices=StudentInGroupStatus.choices(), default='studying')
    student_first_lesson = models.ForeignKey('Lesson', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Guruhdagi o\'quvchi'
        verbose_name_plural = 'Guruhdagi o\'quvchilar'

    def __str__(self) -> str:
        return f'{self.student.first_name}: {self.group.name}'

