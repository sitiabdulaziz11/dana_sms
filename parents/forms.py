from django import forms

from .models import Parent, PhoneNumber, EmergencyContact


class ParentForm(forms.ModelForm):
    """Parent form.
    """
    class Meta:
        model = Parent
        fields = "__all__"
        labels = {
                "city": "City/ከተማ",
                "kfle_ketema": "Subcity/ክፍለ ከተማ",
                "wereda": "Wereda/ወረዳ",
                "hous_number": "Hous Number/የቤት ቁጥር",
                "nationality": "Nationality"
            }

class EmergencyContactForm(forms.ModelForm):
    """ Emergency contact form.
    """
    class Meta:
        model = EmergencyContact
        fields = "__all__"
        labels = {
                "city": "City/ከተማ",
                "kfle_ketema": "Subcity/ክፍለ ከተማ",
                "wereda": "Wereda/ወረዳ",
                "hous_number": "Hous Number/የቤት ቁጥር",
                "nationality": "Nationality"
            }

class PhoneNumberForm(forms.ModelForm):
    """ Phone number form.
    """
    class Meta:
        model = PhoneNumber
        fields = "__all__"
