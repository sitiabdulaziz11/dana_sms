from django import forms
from .models import Payment
from django.forms import modelformset_factory


class PaymentForm(forms.ModelForm):
    """A Django ModelForm for handling student payment data.
    """
    class Meta:
        """Specifies the model associated with the form (Payment)
        """
        model = Payment
        # exclude = ["student"]
        fields = '__all__'
        labels = {
            "payer_name": "Payer Name"
        }

PaymentFormSet = modelformset_factory(Payment, form=PaymentForm, extra=0)
