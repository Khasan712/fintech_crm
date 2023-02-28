from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.commons.models import CustomBaseAbstract
from apps.v1.user.enums import StudentType, UserRole
from apps.v1.user.managers import (
    UserManager,
    SuperAdminManager,
    AdminManager,
    TeacherManager,
    StudentManager
)


class User(AbstractBaseUser, PermissionsMixin, CustomBaseAbstract):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=11, choices=UserRole.choices())
    student_type = models.CharField(max_length=7, choices=StudentType.choices(), blank=True, null=True)

    mother_full_name = models.CharField(max_length=50, blank=True, null=True)
    mother_phone = models.CharField(max_length=50, blank=True, null=True)
    father_full_name = models.CharField(max_length=50, blank=True, null=True)
    father_phone = models.CharField(max_length=50, blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self) -> str:
        return f'{self.phone_number} {self.first_name}'


class SuperAdmin(User):
    objects = SuperAdminManager()

    class Meta:
        proxy = True
        verbose_name = 'Super admin'
        verbose_name_plural = 'Super adminlar'


class Admin(User):
    objects = AdminManager()

    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Adminlar'


class Teacher(User):
    objects = TeacherManager()

    class Meta:
        proxy = True
        verbose_name = 'Ustoz'
        verbose_name_plural = 'Ustozlar'


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"


class RegisterCode(models.Model):
    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=256)
    tries = models.IntegerField(default=0)
    state = models.CharField(max_length=128, default="step_one")
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)

    class Meta:
        verbose_name = "Registratsiya kod"
        verbose_name_plural = "Registratsiya kodlari"

