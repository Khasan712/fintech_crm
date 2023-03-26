from django import forms
from apps.v1.edu.models.groups import StudentProject


class StudentProjectItemForm(forms.ModelForm):
    class Meta:
        model = StudentProject
        fields = ('id', 'name', 'project_card', 'uploaded_file', 'github_link', 'netlify_link')
