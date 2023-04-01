from django.db import models
from apps.commons.models import CustomBaseAbstract
from apps.v1.user.models import User, Student


class BookPresentationQty(models.Model):
    book_qty = models.IntegerField(default=8)

    class Meta:
        verbose_name = "Kitob taqdimoti"
        verbose_name_plural = "Kitob taqdimoti soni"
    
    def __str__(self) -> str:
        return f"Kitob taqdimoti soni - {self.book_qty}"


class StudentBookPresentationCard(CustomBaseAbstract):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_qty = models.IntegerField(default=8)

    def __str__(self) -> str:
        return f"{self.student.first_name} - {self.total_qty}"


class StudentBookPresentation(CustomBaseAbstract):
    book_card = models.ForeignKey(StudentBookPresentationCard, on_delete=models.CASCADE, related_name="student_book_card")
    book = models.CharField(max_length=255)
    is_aproved = models.BooleanField(default=False)
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='book_approver', blank=True)

    class Meta:
        verbose_name = "Kitob taqdimoti"
        verbose_name_plural = "Kitoblar taqdimoti"
    
    def __str__(self):
        return f"{self.book_card.student.first_name} - {self.book}: {self.is_aproved}"
    
    @property
    def get_student(self):
        return f"{self.book_card.student.first_name}"
    

class RentBook(CustomBaseAbstract):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    book = models.CharField(max_length=255)
    deadline_at = models.DateField()
    
    class Meta:
        verbose_name = 'Kitob buyurtma'
        verbose_name_plural = 'Kitob buyurtmalar'
        
    def __str__(self):
        return f'{self.user.first_name} {self.book}'
