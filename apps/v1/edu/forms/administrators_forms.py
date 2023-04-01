from django import forms


from apps.v1.edu.models.groups import Group, GroupStudent


class GroupAddForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = (
            'id', 'name', 'title', 'course', 'teacher', 'group_type', 'monday', 'tuesday',
            'wednesday', 'thursday', 'friday', 'saturday', 'sunday'
        )

