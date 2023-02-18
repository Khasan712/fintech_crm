from django.contrib import admin

from apps.v1.edu.models.courses import Course
from apps.v1.edu.models.groups import Group
from apps.v1.edu.models.lessons import Lesson, Attendance


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course', 'teacher', 'start_time', 'end_time', 'from_term', 'to_term')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'group', 'theme', 'start_time', 'end_time', 'created_at')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'lesson', 'is_come', 'h_m_percentage', 'created_at')


