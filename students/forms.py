from django import forms
from django.forms import inlineformset_factory

from .models import StudentRegistration, Enrollment, AcademicYear


class StudentRegistrationForm(forms.ModelForm):
    """A Django ModelForm for registering new students.
    """
    
    required_css_class = "required"

    class Meta:
        """Specifies the model to use for the form (Student) and
        defines
    which fields to include or exclude.
        """

        model = StudentRegistration
        exclude = ["join_year"]
        labels = {
            "city": "City/ከተማ",
            "kfle_ketema": "Subcity/ክፍለ ከተማ",
            "wereda": "Wereda/ወረዳ",
            "hous_number": "Hous Number/የቤት ቁጥር",
            "nationality": "Nationality"
        }
        # exclude = ["parent"]
        # labels =  {}

class EnrollmentForm(forms.ModelForm):
    """model form for student enrollment.
    """
    class Meta:
        model = Enrollment
        # fields = '__all__'
        # exclude = ["enrollment_date"]
        fields = ['grade', 'section', 'academic_year']

EnrollmentFormSet = inlineformset_factory(
    StudentRegistration,
    Enrollment,
    form=EnrollmentForm,
    extra=0,   # show number o  enrollment form
    can_delete=False,  # enrollment should not be skipped
    validate_min=True,  # ✅ require minimum number
    min_num=1          # ✅ must have at least 1 enrollment
)


class AcademicYearForm(forms.ModelForm):
    """Forms to register academic year.
    """
    class Meta:
        model = AcademicYear
        fields = '__all__'
