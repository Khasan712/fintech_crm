from django import forms
from apps.v1.edu.models.lessons import Lesson


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
    

