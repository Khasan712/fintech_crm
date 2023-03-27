from django import forms
from apps.v1.edu.models.exams import ExamStudentItem
from apps.v1.edu.models.groups import StudentProject


class StudentProjectItemForm(forms.ModelForm):
    class Meta:
        model = StudentProject
        fields = ('id', 'name', 'project_card', 'uploaded_file', 'github_link', 'netlify_link')


class UploadExamItemStudent(forms.ModelForm):
    class Meta:
        model = ExamStudentItem
        fields = ('id', 'uploaded_file', 'netlify_link', 'github_link', 'name')

