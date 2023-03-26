from django import forms
from apps.v1.edu.models.lessons import Lesson
from apps.v1.edu.models.exams import Exam, ExamFile

class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('id', 'theme', 'description')


class UpdateLessonForm(forms.ModelForm):
    status = forms.CharField(required=False)
    class Meta:
        model = Lesson
        fields = ('id', 'theme', 'description', 'status')
    
    # def clean(self):
    #     lesson_status = self.cleaned_data.get('status')
    #     return super().clean()


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ('id', 'name', 'description', 'deadline')


class AddExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ('id', 'name', 'description', 'deadline')



class ExamFileForms(forms.ModelForm):
    class Meta:
        model = ExamFile
        fields = ('id', 'name', 'url_address', 'uploaded_file')
