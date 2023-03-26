from django.contrib import admin

from apps.v1.edu.models.exams import Exam, ExamFile, ExamStudentCard, ExamStudentItem
from apps.v1.edu.models.groups import Group, GroupStudent, StudentProject, StudentProjectsCard
from apps.v1.edu.models.courses import Course
from apps.v1.edu.models.lessons import HomeTaskItem, Lesson, Attendance, OnlyHomeTask, SubjectGuide
from apps.v1.edu.models.presentations import BookPresentationQty, StudentBookPresentation, StudentBookPresentationCard


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course', 'teacher', 'start_time', 'end_time', 'from_term', 'to_term')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'group', 'theme', 'start_time', 'end_time', 'created_at', 'creator', 'updater', 'deleter')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'lesson', 'is_come', 'h_m_percentage', 'created_at')


@admin.register(GroupStudent)
class GroupStudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'group', 'created_at')


@admin.register(SubjectGuide)
class SubjectGuideAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'teacher', 'deadline')


@admin.register(OnlyHomeTask)
class OnlyHomeTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'teacher', 'deadline')


@admin.register(HomeTaskItem)
class HomeTaskItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'home_task')


@admin.register(StudentBookPresentation)
class StudentBookPresentationAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_card', 'get_student', 'book', 'is_aproved', 'approver')


@admin.register(BookPresentationQty)
class BookPresentationQtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_qty')


@admin.register(StudentBookPresentationCard)
class StudentBookPresentationCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'total_qty',)


@admin.register(StudentProjectsCard)
class StudentProjectsCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'group', 'course_projects_qty')

@admin.register(StudentProject)
class StudentProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_card', 'uploaded_file')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'name', 'created_at', 'deadline')


@admin.register(ExamFile)
class ExamFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam', 'uploaded_file', 'created_at')


@admin.register(ExamStudentCard)
class ExamStudentCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam', 'student', 'exam_point', 'created_at')


@admin.register(ExamStudentItem)
class ExamStudentItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam_card', 'name', 'github_link', 'created_at')