from django.shortcuts import render, redirect, get_object_or_404
from formtools.wizard.views import SessionWizardView
from django.forms import modelformset_factory

from .forms import ParentForm, PhoneNumberForm, EmergencyContactForm
from .models import Parent, PhoneNumber

# Create your views here.

FORMS = [
    ("parent_info", ParentForm),
    ("phoneNumber_info", PhoneNumberForm),
    ("emergencyContact_info", EmergencyContactForm),
]

TEMPLATES = {
    "parent_info": "parents/parent_enroll.html",
    "phoneNumber_info": "parents/phone_enroll.html",
    "emergencyContact_info": "parents/contact_enroll.html",
}

class ParentEnrollmentWizard(SessionWizardView):
    """ Views to handel different form step of registration.
    """
    form_list = FORMS
    # template_name = "parents/enrollment.html"

    def get_template_names(self):
        """
        """
        return [TEMPLATES[self.steps.current]]
    
    def done(self, form_list, **kwargs):
        """
        """
        parent_form = form_list[0]
        phoneNum_form = form_list[1]
        emergencyCon_form = form_list[2]

        parent = parent_form.save(commit=False)
        parent.save()

        phone = phoneNum_form.save(commit=False)
        phone.parent = parent
        phone.save()

        emergency = emergencyCon_form.save(commit=False)
        emergency.parent = parent
        emergency.save()
        
        return redirect("success_page")


def parent_info(request):
    """Views for parent information.
    """
    if request.method == "POST":
        form = ParentForm(request.POST)
        if form.is_valid():
            parent = form.save()  # commit to DB
            request.session["parent_id"] = parent.id  # store for next steps

            if "add_another" in request.POST:
                return redirect("prnt_info")
            else:
                return redirect("phone_info")  # go to next step
    else:
        form = ParentForm()
    return render(request, "parents/parent_enroll.html", {
        "form": form
    })

# PhoneFormSet = modelformset_factory(PhoneNumber, fields=("parent", "number", "owner", "number_type"), extra=2)

def phoneNum_info(request):
    """For phone number
    """
    parent_id = request.session.get("parent_id")
    parent = get_object_or_404(Parent, id=parent_id)

    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone = form.save(commit=False)
            phone.parent = parent
            phone.save()

            # Check which button was clicked
            if "add_another" in request.POST:
                # Reload the same page for adding another phone
                return redirect("phone_info")
            else:
                # Move to the next step (emergency contact)
                return redirect("emrgncy_info")
    else:
        form = PhoneNumberForm()

    # Display all saved phones for this parent
    phones = PhoneNumber.objects.filter(parent=parent)
    return render(request, "parents/phone_enroll.html", {
        "form": form,
        "phones": phones
        })
   
    # if request.method == "POST":
    #     formset = PhoneFormSet(request.POST, queryset=PhoneNumber.objects.none())
    #     if formset.is_valid():
    #         phones = formset.save(commit=False)
    #         for phone in phones:
    #             phone.parent = parent
    #             phone.save()
    #         return redirect("emergency_step")
    # else:
    #     formset = PhoneFormSet(queryset=PhoneNumber.objects.none())
    # return render(request, "parents/phone_enroll.html", {"formset": formset})

def emergency_info(request):
    """For phone number
    """
    parent_id = request.session.get("parent_id")
    parent = get_object_or_404(Parent, id=parent_id)

    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone = form.save(commit=False)
            phone.parent = parent
            phone.save()

            # Check which button was clicked
            if "add_another" in request.POST:
                # Reload the same page for adding another phone
                return redirect("phone_info")
            else:
                # Move to the next step (emergency contact)
                return redirect("emergency_step")
    else:
        form = PhoneNumberForm()

    # Display all saved phones for this parent
    phones = PhoneNumber.objects.filter(parent=parent)
    return render(request, "parents/phone_enroll.html", {"form": form, "phones": phones})
