from django.contrib.auth.models import BaseUserManager
from django.db.models import manager


class UserManager(BaseUserManager):

    def create_user(self, first_name, last_name, phone_number, role, password, **extra_fields):

        if not first_name:
            raise ValueError('The first name must be fill.')
        if not last_name:
            raise ValueError('The last name must be fill.')
        if not phone_number:
            raise ValueError('The phone number must be fill.')
        if not role:
            raise ValueError('The user role must be fill.')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, phone_number, role, password, **extra_fields):
        """
            Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role=role,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save(using=self._db)
        return user


class SuperAdminManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="super_admin")


class AdministratorManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="administrator")


class TeacherManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="teacher")


class StudentManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="student", is_verified=True)
    
class StudentNotVerifiedManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="student", is_verified=False)
