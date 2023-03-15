from django.db import models

from apps.commons.models import CustomBaseAbstract
from apps.v1.edu.enums import StudentProjectStatus
from apps.v1.edu.models.groups import Group
from apps.v1.user.models import Student

class Exam(CustomBaseAbstract):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255)
    deadline = models.DateTimeField()

    class Meta:
        verbose_name = 'Imtoxon'
        verbose_name_plural = 'Imtoxonlar'
    
    def __str__(self) -> str:
        return f'{self.name} - {self.group.name}'


class ExamStudentCard(CustomBaseAbstract):
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    exam_point = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'O\'quvchi imtixon kart'
        verbose_name_plural = 'O\'quvchilar imtixon kartlari'
    
    def __str__(self) -> str:
        return f'{self.student.first_name} - {self.exam.name}'


class ExamStudentItem(CustomBaseAbstract):
    exam_card = models.ForeignKey(ExamStudentCard, on_delete=models.SET_NULL, null=True)
    uploaded_file = models.FileField(upload_to='exam/')
    netlify_link = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=11, choices=StudentProjectStatus.choices(), default='in_progress')
    name = models.CharField(max_length=255)
    github_link = models.URLField()

    class Meta:
        verbose_name = 'O\'quvchi imtixon yuklagan fayl'
        verbose_name_plural = 'O\'quvchilar imtixon yuklagan fayllari'

    def __str__(self) -> str:
        return f'{self.exam_card.student.first_name} - {self.status}'