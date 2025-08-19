from django import forms

from .models import Grade, Section

class GradeForm(forms.ModelForm):
    """form used to register grade.
    """
    class Meta:
        model = Grade
        fields = "__all__"

class SectionForm(forms.ModelForm):
    """form used to register section.
    """
    class Meta:
        model = Section
        fields = "__all__"

# class GradeSectionForm(forms.Form):
#     """forms to register Grade and Section.
#     """
#     grade_name = forms.CharField(max_length=30, label="Grade Name")
#     section_name = forms.CharField(max_length=30, label="Section Name")
