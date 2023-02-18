from enum import Enum


class UserRole(Enum):
    super_admin = 'super_admin'
    admin = 'admin'
    teacher = 'teacher'
    student = 'student'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
