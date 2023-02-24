
from django.db import models
from django.forms import ValidationError
from apps.commons.enums import LessonStatus

from apps.commons.models import CustomBaseAbstract, CustomWeekAbstract
from apps.v1.edu.models.groups import Group
from apps.v1.user.models import Student


class Lesson(CustomBaseAbstract):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    theme = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(blank=True, null=True)
    lesson_number = models.IntegerField(default=0)
    status = models.CharField(max_length=8, choices=LessonStatus.choices(), default='started')
    creator = models.ForeignKey(
        'user.User', models.SET_NULL, null=True, related_name='lesson_creator'
    )
    updater = models.ForeignKey(
        'user.User', models.SET_NULL, null=True, blank=True, editable=False, related_name='lesson_updater'
    )
    deleter = models.ForeignKey(
        'user.User', models.SET_NULL, null=True, blank=True, editable=False, related_name='lesson_deleter'
    )


    class Meta:
        verbose_name = 'Dars'
        verbose_name_plural = 'Darslar'
    
    def save(self, *args, **kwargs):
        if self.lesson_number == 0:
            self.lesson_number = Lesson.objects.select_related('group', 'creator', 'updater', 'deleter').count() + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id} - {self.group.name}'


class Attendance(CustomBaseAbstract):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_attendance')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    is_come = models.BooleanField(default=False)
    h_m_percentage = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Davomat'
        verbose_name_plural = 'Davomatlar'

    def clean(self) -> None:
        if self.h_m_percentage < 0 or self.h_m_percentage > 10:
            raise ValidationError("Can not!")

    def save(self, *args, **kwargs):
        super().full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id} - {self.student.first_name}'

class HomeTask(CustomBaseAbstract):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(
        'user.User', models.SET_NULL, null=True, related_name='home_task_teacher'
    )
    deadline = models.DateTimeField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Uy ishi'
        verbose_name_plural = 'Uy ishilar'

    def __str__(self):
        return f'{self.lesson} - {self.teacher.first_name}'
    

class HomeTaskItem(CustomBaseAbstract):
    home_task = models.ForeignKey(HomeTask, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True, null=True)
    uploaded_file = models.FileField(upload_to='home_tasks/', blank=True, null=True)

    class Meta:
        verbose_name = 'Topshiriq'
        verbose_name_plural = 'Topshiriqlar'


class HomeWork(CustomBaseAbstract):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_homework')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Uy ishi javobi'
        verbose_name_plural = 'Uy ishi javobilari'


class HomeWorkItem(CustomBaseAbstract):
    home_work = models.ForeignKey(HomeWork, models.SET_NULL, null=True)
    task = models.ForeignKey(HomeTaskItem, models.SET_NULL, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    uploaded_file = models.FileField(upload_to='home_tasks/', blank=True, null=True)

    class Meta:
        verbose_name = 'Topshiriq javobi'
        verbose_name_plural = 'Topshiriqlar javoblari'
