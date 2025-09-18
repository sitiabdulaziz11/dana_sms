from django import forms

from .models import Parent, PhoneNumber, EmergencyContact
from django.forms import modelformset_factory, inlineformset_factory


class ParentForm(forms.ModelForm):
    """Parent form.
    """
    class Meta:
        model = Parent
        # fields = "__all__"
        exclude = ["children"]
        labels = {
                "city": "City/ከተማ",
                "kfle_ketema": "Subcity/ክፍለ ከተማ",
                "wereda": "Wereda/ወረዳ",
                "hous_number": "Hous Number/የቤት ቁጥር",
                "nationality": "Nationality"
            }
    
    def __init__(self, *args, require_fields=True, **kwargs):
        """
        require_fields=True → mandatory fields enforced (new parent case)
        require_fields=False → all fields optional (existing parent case)
        """
        super().__init__(*args, **kwargs)

        if not require_fields:
            for field in self.fields.values():
                field.required = False
    
ParentFormSet = modelformset_factory(
    Parent,
    form=ParentForm,  # to reuse custom forms
    extra=0,   # no empty form
    can_delete=True
)


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

EmergencyContactFormSet = modelformset_factory(
    EmergencyContact,
    form=EmergencyContactForm,  # to reuse custom forms
    extra=0,   # no empty form
    can_delete=True
)


class PhoneNumberForm(forms.ModelForm):
    """ Phone number form.
    """
    class Meta:
        model = PhoneNumber
        fields = "__all__"

PhoneFormSet = inlineformset_factory(
    Parent,         # parent model
    PhoneNumber,    # child model
    form=PhoneNumberForm,
    extra=0,
    can_delete=True
)
