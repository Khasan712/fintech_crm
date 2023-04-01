from apps.v1.user.models import Student, Teacher
from apps.v1.edu.models.courses import Course
from apps.v1.edu.models.presentations import RentBook, StudentBookPresentationCard, StudentBookPresentation
from apps.v1.edu.models.exams import Exam, ExamFile, ExamStudentCard, ExamStudentItem
from apps.v1.edu.models.groups import Group, GroupStudent, StudentProject, StudentProjectsCard
from apps.v1.edu.models.lessons import Attendance, HomeTask, HomeTaskItem, HomeWork, HomeWorkItem, Lesson


def get_students_queryset(self):
    return Student.objects.all()


def get_group_queryset(self):
    return Group.objects.select_related('course', 'teacher', 'creator', 'updater', 'deleter')


def get_student_in_group_queryset(self):
    return GroupStudent.objects.select_related('student', 'group', 'student_first_lesson', 'creator', 'updater', 'deleter')


def get_course_queryset(self):
    return Course.objects.all()


def get_teacher_queryset(self):
    return Teacher.objects.all()


def get_attendance_queryset(self):
    return Attendance.objects.select_related('student', 'lesson')


def get_rent_books_queryset(self):
    return RentBook.objects.select_related('user')


def get_lessons_queryset(self):
    return Lesson.objects.select_related('group', 'creator', 'updater', 'deleter')


def get_hometask_queryset(self):
    return HomeTask.objects.select_related('lesson', 'teacher')


def get_hometask_items_queryset(self):
    return HomeTaskItem.objects.select_related('home_task')


def get_homework_queryset(self):
    return HomeWork.objects.select_related('student', 'lesson')


def get_homework_items_queryset(self):
    return HomeWorkItem.objects.select_related('home_work', 'task')


def get_student_projects_card_queryset(self):
    return StudentProjectsCard.objects.select_related("student", "group")


def get_student_projects(self):
    return StudentProject.objects.select_related("project_card")


def get_book_presentation_queryset(self):
    return StudentBookPresentationCard.objects.select_related('student')


def get_book_presentation_item_queryset(self):
    return StudentBookPresentation.objects.select_related("book_card", 'approver')


def get_exam_queryset(self):
    return Exam.objects.select_related('group')


def get_exam_file_queryset(self):
    return ExamFile.objects.select_related("exam")


def get_student_exam_item_queryset(self):
    return ExamStudentItem.objects.select_related('exam_card')


def get_student_exam_card_queryset(self):
    return ExamStudentCard.objects.select_related('exam', 'student')