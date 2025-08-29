from django.shortcuts import render, redirect, get_object_or_404
from formtools.wizard.views import SessionWizardView
from django.forms import modelformset_factory
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.urls import reverse


from .forms import ParentForm, PhoneNumberForm, EmergencyContactForm
from .models import Parent, PhoneNumber
from students.models import StudentRegistration

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
    # reset review mode when starting fresh
    if "review_mode" in request.session:
        del request.session["review_mode"]

    if request.method == "POST":
        form = ParentForm(request.POST)

        if form.is_valid():
            parent = form.save()  # commit to DB
            request.session["parent_ids"] = [parent.id]  # store for next steps

            if "review_mode" in request.session:
                return redirect("review")

            if "add_another" in request.POST:
                return redirect("prnt_info")
            else:
                return redirect("phone_info")  # go to next step
            
    else:
        form = ParentForm()
    return render(request, "parents/parent_enroll.html", {
        "form": form,
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
            request.session["phone_ids"] = [phone.id]

            if "review_mode" in request.session:
                return redirect("review")

            # Check which button was clicked
            if "add_another" in request.POST:
                # Reload the same page for adding another phone
                return redirect("phone_info")
            else:
                # Move to the next step (emergency contact)
                return redirect("register")
    else:
        form = PhoneNumberForm()

    # Display all saved phones for this parent
    # phones = PhoneNumber.objects.filter(parent=parent)
    return render(request, "parents/phone_enroll.html", {
        "form": form,
        "back_url": reverse("prnt_info")
        # "phones": phones
        })

def emergency_info(request):
    """For phone number
    """
    parent_id = request.session.get("parent_id")
    if not parent_id:
        return HttpResponse("no parent id")
    
    student_id = request.session.get("student_id")
    if not student_id:
        # return HttpResponse("no student id")
        return redirect("register")  # Redirect to student registration
    
    parent = get_object_or_404(Parent, id=parent_id)
    student = get_object_or_404(StudentRegistration, id=student_id)

    if request.method == "POST":
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            emergency = form.save(commit=False)
            emergency.parent = parent
            emergency.save()
            request.session["emergency_ids"] = [emergency.id]

            if "review_mode" in request.session:
                return redirect("review")

            # Check which button was clicked
            if "add_another" in request.POST:
                # Reload the same page for adding another phone
                return redirect("emrgncy_info")
            else: 
                # Move to the next step (emergency contact)
                return redirect("pay_with_id", student_id=student.id)
    else:
        form = EmergencyContactForm()

    # Display all saved phones for this parent
    # phones = PhoneNumber.objects.filter(parent=parent)
    return render(request, "parents/emergency_enroll.html", {"form": form}) #"phones": phones})
