from enum import Enum


class UserRole(Enum):
    super_admin = 'super_admin'
    administrator = 'administrator'
    teacher = 'teacher'
    student = 'student'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class StudentType(Enum):
    online = 'online'
    offline = 'offline'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
