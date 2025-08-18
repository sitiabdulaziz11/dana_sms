from django import forms
from .models import StudentRegistration


class StudentRegistrationForm(forms.ModelForm):
    """A Django ModelForm for registering new students.
    """
    class Meta:
        """Specifies the model to use for the form (Student) and
        defines
    which fields to include or exclude.
        """
        model = StudentRegistration
        exclude = ["join_year"]
        labels = [
            "kebele_wereda": "Wo"
            "kfleketema", "hous_number", "nationality"
        ]
        # exclude = ["parent"]
        # labels =  {}
