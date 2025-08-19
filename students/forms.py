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
        labels = {
            "city": "City/ከተማ",
            "kfle_ketema": "Subcity/ክፍለ ከተማ",
            "wereda": "Wereda/ወረዳ",
            "hous_number": "Hous Number/የቤት ቁጥር",
            "nationality": "Nationality"
        }
        # exclude = ["parent"]
        # labels =  {}
