from django.db import models

from apps.commons.models import CustomBaseAbstract, CustomWeekAbstract
from apps.v1.edu.enums import GroupStatus, GroupType, StudentInGroupStatus, StudentProjectStatus
from apps.v1.edu.models.courses import Course
from apps.v1.user.enums import StudentType
from apps.v1.user.models import Student, User, Teacher


class Group(CustomBaseAbstract, CustomWeekAbstract):
    """ Group """
    name = models.CharField(max_length=70)
    title = models.CharField(max_length=255, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='group_course')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='group_teacher')
    group_status = models.CharField(max_length=8, choices=GroupStatus.choices(), default='active')
    group_type = models.CharField(max_length=8, choices=GroupType.choices(), default='hibrid')
    
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='group_creator')
    updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='group_updater', blank=True)
    deleter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='group_deleter', blank=True)

    start_time = models.TimeField()
    end_time = models.TimeField()
    from_term = models.DateField(blank=True, null=True)
    to_term = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Guruh'
        verbose_name_plural = 'Guruhlar'

    def __str__(self):
        return f'{self.id} - {self.name}'


class GroupStudent(CustomBaseAbstract):
    """ Group students """
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='student_in_group')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_of_student')
    student_status = models.CharField(max_length=8, choices=StudentInGroupStatus.choices(), default='studying')
    student_type = models.CharField(max_length=7, choices=StudentType.choices(), blank=True, null=True)
    student_first_lesson = models.ForeignKey('Lesson', on_delete=models.SET_NULL, null=True, blank=True)
    
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='group_creator_student')
    updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='group_updater_student', blank=True)
    deleter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='group_deleter_student', blank=True)

    class Meta:
        verbose_name = 'Guruhdagi o\'quvchi'
        verbose_name_plural = 'Guruhdagi o\'quvchilar'

    def __str__(self) -> str:
        return f'{self.student.first_name}: {self.group.name}'


class StudentProjectsCard(CustomBaseAbstract):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='student_projects_card')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='student_projects_card_group')
    course_projects_qty = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'O\'quvchi loyiha kart'
        verbose_name_plural = 'O\'quvchilar loyiha kart'
    
    def __str__(self) -> str:
        return f'{self.student.first_name} - {self.group.name}'


class StudentProject(CustomBaseAbstract):
    name = models.CharField(max_length=255)
    project_card = models.ForeignKey(StudentProjectsCard, on_delete=models.SET_NULL, null=True, related_name="student_project_item")
    uploaded_file = models.FileField(upload_to='projects/')
    github_link = models.URLField()
    netlify_link = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=11, choices=StudentProjectStatus.choices(), default='in_progress')

    class Meta:
        verbose_name = 'O\'quvchi loyihasi'
        verbose_name_plural = 'O\'quvchilar loyihalari'

    def __str__(self) -> str:
        return f'{self.project_card.student.first_name} - {self.status}'
    

