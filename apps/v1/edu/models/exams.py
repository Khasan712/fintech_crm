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

    @property
    def get_formated_deadline(self):
        return self.deadline.strftime('%Y-%m-%dT%H:%M')


class ExamFile(CustomBaseAbstract):
    name = models.CharField(max_length=255)
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True)
    uploaded_file = models.FileField(upload_to='exam/', blank=True, null=True)
    url_address = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Imtixon fayli'
        verbose_name_plural = 'Imtixon fayllar'


class ExamStudentCard(CustomBaseAbstract):
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, related_name='exam_item')
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name="student_exam_card")
    exam_point = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'O\'quvchi imtixon kart'
        verbose_name_plural = 'O\'quvchilar imtixon kartlari'

    def __str__(self) -> str:
        return f'{self.student.first_name} - {self.exam.name}'


class ExamStudentItem(CustomBaseAbstract):
    exam_card = models.ForeignKey(ExamStudentCard, on_delete=models.SET_NULL, null=True, related_name='student_item_exam_card')
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