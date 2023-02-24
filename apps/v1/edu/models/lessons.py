
from django.db import models
from apps.commons.enums import LessonStatus

from apps.commons.models import CustomBaseAbstract, CustomWeekAbstract
from apps.v1.edu.models.groups import Group
from apps.v1.user.models import Student


class Lesson(CustomBaseAbstract):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    theme = models.CharField(max_length=255)
    start_time = models.TimeField()
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
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    is_come = models.BooleanField()
    h_m_percentage = models.FloatField(default=0)

    class Meta:
        verbose_name = 'Davomat'
        verbose_name_plural = 'Davomatlar'

    def __str__(self):
        return f'{self.id} - {self.student.first_name}'


# class Home


class HometaskCart(models.Model):
    teacher = models.CharField(max_length=128)
    deadline = models.DateField()
    lesson = models.CharField(max_length=128)
    text = models.TextField()

class HometaskItem(models.Model):
    text = models.TextField()
    file = models.FileField(upload_to="Hometask")
    hometaskcart = models.ForeignKey(HometaskCart,on_delete=models.CASCADE)


class Homework(models.Model):
    student = models.CharField(max_length=128)
    ball = models.IntegerField()
    lesson = models.CharField()
    hometask = models.ForeignKey(HometaskItem,on_delete=models.CASCADE)
class File(models.Model):
    file = models.FileField(upload_to="Homework")
    hometaskitem = models.ForeignKey(HometaskItem,on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework,on_delete=models.CASCADE)