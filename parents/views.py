from django.shortcuts import render, redirect, get_object_or_404
from formtools.wizard.views import SessionWizardView
from django.forms import modelformset_factory
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings


from .forms import ParentForm, PhoneNumberForm, EmergencyContactForm
from .models import Parent, PhoneNumber
from students.models import StudentRegistration
from students.forms import StudentRegistrationForm
from payments.forms import PaymentForm
from payments.models import Payment

# Create your views here.

FORMS = [
    ("parent_info", ParentForm),
    ("phoneNumber_info", PhoneNumberForm),
    ("register_student", StudentRegistrationForm),
    ("emergency_info", EmergencyContactForm),
    ("make_payment", PaymentForm),
]

TEMPLATES = {
    "parent_info": "parents/parent_enroll.html",
    "phoneNumber_info": "parents/phone_enroll.html",
    "register_student": "students/registration.html",
    "emergency_info": "parents/emergency_enroll.html",
    "make_payment": "payments/make_payment.html",
}

STEPS = ["parent", "phone", "student", "emergency", "payment"]

file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'tmp'))

class ParentEnrollmentWizard(SessionWizardView):
    """ Views to handel different form step of registration.
    """
    form_list = FORMS
    file_storage = file_storage
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
        student_form = form_list[2]
        emergencyCon_form = form_list[3]
        Payment_form = form_list[4]

        parent = parent_form.save(commit=False)
        parent.save()

        phone = phoneNum_form.save(commit=False)
        phone.parent = parent
        phone.save()

        student = student_form.save(commit=False)
        student.parent = parent
        student.save()

        emergency = emergencyCon_form.save(commit=False)
        emergency.parent = parent
        emergency.save()

        Payment_form = Payment_form.save(commit=False)
        Payment_form.parent = parent
        Payment_form.save()
        
        return redirect("success_page")


def parent_info(request):
    """Views for parent information.
       Select existing parents or add new ones for the student
    """
    if "review_mode" in request.session:
        del request.session["review_mode"]   # reset review mode when starting fresh
    if "parent_ids" not in request.session:
        request.session["parent_ids"] = []  # reset in a new student registration.

    parent_ids = request.session.get("parent_ids", [])
    
    if request.method == "POST":
        # 2️⃣ Add selected existing parents
        selected_parents = request.POST.getlist("existing_parents")

        fields_to_check = [
            name for name, field in ParentForm().fields.items() if field.required
            ]
        filled_new_parent = (
            any(request.POST.get(f, '').strip() for f in fields_to_check)
            or bool(request.FILES.get('image_file'))
            )

        if not filled_new_parent and not selected_parents:
            messages.error(request, "Please add a new parent or select an existing one .")
            form = ParentForm()  # so form is rendered
            all_parents = Parent.objects.all()
            return render(request, "parents/parent_enroll.html", {
                "form": form,
                "all_parents": all_parents,
                })

        # 1️⃣ Add new parent
        if filled_new_parent:
            form = ParentForm(request.POST, request.FILES)
            if form.is_valid():
                new_parent = form.save()  # commit to DB
                if new_parent.id not in parent_ids:
                    parent_ids.append(new_parent.id)

                # Set the current parent ID to the newly added parent
                request.session["current_parent_id"] = new_parent.id
        # else:
        #     form = ParentForm()   #  # If no new parent data was filled → skip form validation
        
        for pid in selected_parents:
            if int(pid) not in parent_ids:
                parent_ids.append(int(pid))
        
        request.session["parent_ids"] = parent_ids  # store for next steps
        print("SESSION parent_ids:", request.session.get("parent_ids"))

        request.session["current_step"] = request.session.get("current_step", 0) + 1
        request.session.modified = True

        if "review_mode" in request.session:
            return redirect("review")

        if "add_another" in request.POST:
            return redirect("prnt_info")
        else:
            return redirect("phone_info")  # go to next step
    else:
        form = ParentForm()
        # Fetch existing parents for dropdown/multi-select
        all_parents = Parent.objects.all()

        request.session["current_step"] = 1
        request.session.modified = False

        # optional to print session ?
    # parent_ids = request.session.get("parent_ids", [])
    # parents_added = Parent.objects.filter(id__in=parent_ids)

    return render(request, "parents/parent_enroll.html", {
        "form": form,
        "all_parents": all_parents,
        # "parents_added": parents_added,
        # "current_step": current_step,
        # "total_step": total_step
    })

def phoneNum_info(request):
    """For phone number
    """
    # current_step = request.session.get("current_step", 1)
    # total_step = request.session.get("total_steps", 5)
    # # total_step = len(STEPS)
    # # current_step = STEPS.index("phone") + 1

    if "phone_ids" not in request.session:
        request.session["phone_ids"] = []

    current_parent_id = request.session.get("current_parent_id")
    if not current_parent_id:
        messages.error(request, "No parent found in session. Please register a parent first.")
        return redirect("prnt_info")
    
    parent_c = get_object_or_404(Parent, id=current_parent_id)

    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone = form.save(commit=False)
            parent_id = request.POST.get("parent")  # parent's ID from the form
            # # Make sure parent belongs to this student’s session
            # if int(phone.parent_id) in request.session.get("parent_ids", []):
            #     phone.save()  to check for existing parent
            phone.parent_id = parent_id
            phone.save()
            
            parent = get_object_or_404(Parent, id=parent_id)  # To get current selected/saved parent.

            phone_ids = request.session.get("phone_ids", {})
            if not isinstance(phone_ids, dict):
                phone_ids = {}
            if parent_id not in phone_ids:
                phone_ids[parent_id] = []
                phone_ids[parent_id].append(phone.id)
                request.session["phone_ids"] = phone_ids
                
                print("SESSION parent_ids:", request.session.get("parent_ids"), "phone ids", request.session.get("phone_ids"))

            messages.success(request, f"Phone number added for {parent.first_name}.successfully.")

            request.session["current_step"] = request.session.get("current_step", 1) + 1
            request.session.modified = True

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
        request.session["current_step"] = 2
        request.session.modified = False

    # Display all saved phones for this parent
    phones = PhoneNumber.objects.filter(parent=parent_c)
    return render(request, "parents/phone_enroll.html", {
        "form": form,
        # "back_url": reverse("prnt_info")
        "phones": phones,
        # "current_step": current_step,
        # "total_step": total_step,
        })

def emergency_info(request):
    """For phone number
    """
    if "emergency_ids" not in request.session:
        request.session["emergency_ids"] = []

    # current_parent_id = request.session.get("current_parent_id")
    # if not current_parent_id:
    #     messages.error(request, "from emergency contact, No parent found in session. Please register a parent first.")
    #     return redirect("prnt_info")
    
    student_id = request.session.get("student_id")
    if not student_id:
        messages.error(request, "No student found. Please register a student first.")
        # return HttpResponse("no student id")
        return redirect("register")  # Redirect to student registration
    
    # parent_id = parent_ids[-1]
    # parent = get_object_or_404(Parent, id=parent_ids)
    student = get_object_or_404(StudentRegistration, id=student_id)

    if request.method == "POST":
        form = EmergencyContactForm(request.POST, request.FILES)
        if form.is_valid():
            emergency = form.save(commit=False)
            emergency.student = student
            emergency.save()

            emergency_ids= request.session.get("emergency_ids", [])
            emergency_ids.append(emergency.id)
            request.session["emergency_ids"] = emergency_ids

            request.session["current_step"] = request.session.get("current_step", 1) + 1
            request.session.modified = True

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
        request.session["current_step"] = 4
        request.session.modified = False

    # Display all saved phones for this parent
    # phones = PhoneNumber.objects.filter(parent=parent)
    return render(request, "parents/emergency_enroll.html", {
        "form": form,
       }) #"phones": phones})
