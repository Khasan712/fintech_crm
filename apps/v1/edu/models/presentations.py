from django.db import models
from apps.commons.models import CustomBaseAbstract
from apps.v1.user.models import Student

class StudentBookPresentation(CustomBaseAbstract):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.student.first_name} - {self.book}: {self.is_active}"
    
