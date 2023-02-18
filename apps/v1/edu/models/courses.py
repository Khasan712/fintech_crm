from django.db import models
from apps.commons.models import CustomBaseAbstract


class Course(CustomBaseAbstract):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Kurslar'
        verbose_name = 'Kurs'

    def __str__(self):
        return f'{self.id} - {self.name}'
