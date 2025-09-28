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


from .forms import ParentForm, PhoneNumberForm, EmergencyContactForm, ExistingEmergencyContactForm
from .models import Parent, PhoneNumber, EmergencyContact
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
    selected_parents = []
    all_parents = Parent.objects.all()  # Fetch existing parents for dropdown/multi-select

    if request.method == "POST":
        choice = request.POST.get("form_type")

        # 1️⃣ Add selected existing
        if choice == "existing":
            selected_parents = request.POST.getlist("existing_parents")
            print("Selected parents:", selected_parents)
            if selected_parents:
                for pid in selected_parents:
                    pid = int(pid)
                    if int(pid) not in parent_ids:
                        parent_ids.append(int(pid))
                request.session["parent_ids"] = parent_ids
                print("SESSION parent_ids:", request.session.get("parent_ids"))

                if "review_mode" in request.session:
                    return redirect("review")
                if "add_another" in request.POST:
                    return redirect("prnt_info")
                else:
                    # messages.success(request, "Existing parent(s) linked successfully.")
                    return redirect("register")
            else:
                messages.error(request, "Please select at least one parent")
                return redirect("prnt_info")
            
        # 2️⃣ Add new parent
        elif choice == "new":
            form = ParentForm(request.POST, request.FILES)
            if form.is_valid():
                new_parent = form.save()  # commit to DB
                if new_parent.id not in parent_ids:
                    parent_ids.append(new_parent.id)

                request.session["current_parent_id"] = new_parent.id
                request.session["parent_ids"] = parent_ids
                
                print("SESSION parent_ids:", request.session.get("parent_ids"))

                if "review_mode" in request.session:
                    return redirect("review")

                if "add_another" in request.POST:
                    return redirect("prnt_info")
                
                messages.success(request, "New parent added successfully.")
                return redirect("phone_info")
            else:
                messages.error(request, "Please fill all required fields for the new parent")
        
        else:
            messages.error(request, "Please add a New Parent Or Select From Existing One")
            return redirect("prnt_info")                   
            
        request.session["parent_ids"] = parent_ids  # store for next steps

        request.session["current_step"] = request.session.get("current_step", 0) + 1
        request.session.modified = True

    else:
        form = ParentForm()
        selected_parents = Parent.objects.filter(id__in=parent_ids)  # Pass previously selected parents

        request.session["current_step"] = 1
        request.session.modified = False

    return render(request, "parents/parent_enroll.html", {
        "form": form,
        "all_parents": all_parents,
        "selected_parents": selected_parents,
    })


def phoneNum_info(request):
    """For phone number handling.
    """
    if "phone_ids" not in request.session:
        request.session["phone_ids"] = []

    current_parent_id = request.session.get("current_parent_id")
    if not current_parent_id:
        messages.error(request, "No parent found in session. Please register a parent first.")
        return redirect("prnt_info")
    
    parent_c = get_object_or_404(Parent, id=current_parent_id)
    print("current parent", parent_c)  # debug

    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone = form.save(commit=False)
            parent_id = request.POST.get("parent")  # parent's ID from the form
            print(request.POST)  # debug
            print(parent_id)  # debug
            
            # Make sure parent belongs to this student’s session
            if not int(phone.parent_id) in request.session.get("parent_ids", []):
                messages.error(request, "The selected parent is not associated with the current student. Please select the correct one.")
                return redirect("phone_info")
            
            phone.parent_id = parent_id
            phone.save()

            parent = get_object_or_404(Parent, id=parent_id)  # To get current selected/saved parent.
            messages.success(request, f"Phone number added for {parent.first_name}.successfully.")

            phone_ids = request.session.get("phone_ids", {})
            if not isinstance(phone_ids, dict):
                phone_ids = {}

            if parent_id not in phone_ids:
                phone_ids[parent_id] = []
                
            phone_ids[parent_id].append(phone.id)
            request.session["phone_ids"] = phone_ids
                
            print("SESSION parent_ids:", request.session.get("parent_ids"), "phone ids", request.session.get("phone_ids"))
            
            request.session["current_step"] = request.session.get("current_step", 1) + 1
            request.session.modified = True

            if "review_mode" in request.session:
                return redirect("review")

            # Check which button was clicked
            if "add_another" in request.POST:
                return redirect("phone_info")   # Reload the same page for adding another phone
            else:
                request.session.pop("current_parent_id", None) 
                return redirect("register")   # Move to the next step (emergency contact)
    else:
        form = PhoneNumberForm()
        request.session["current_step"] = 2
        request.session.modified = False

    phones = PhoneNumber.objects.filter(parent=parent_c) # Display all saved phones for this parent

    return render(request, "parents/phone_enroll.html", {
        "form": form,
        "phones": phones,
        "parent_c": parent_c
        })

def emergency_info(request):
    """For emergency handiling.
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
        return redirect("register")  # Redirect to student registration
    
    # parent_id = parent_ids[-1]
    # parent = get_object_or_404(Parent, id=parent_ids)

    student = get_object_or_404(StudentRegistration, id=student_id)
    student_id_get = request.POST.get("student")
    if student_id_get:
        student_id_get = int(student_id_get)

    print("_id", student_id_get)  #  debug
    print(".id", student.id)  #  debug

    parents = student.parents.all()
    # phone = parent.phone_numbers.all() # works for one parent.
    print("Parents queryset1:", list(parents))

    phone = PhoneNumber.objects.filter(parent__in=parents)  # to get many parents phone no at once.

    if request.method == "POST":
        new_form = EmergencyContactForm(request.POST, request.FILES)
        existing_form = ExistingEmergencyContactForm(request.POST)

        saved_ids = []  # Keep track of what was saved this round

        if existing_form.is_valid():
            parent = existing_form.cleaned_data.get("parent")
            print("Chosen parent:", parent)  #  debug
            print("Check:", parent in parents)  #  debug

            phone = existing_form.cleaned_data.get("phone_num")
            print(phone)  #  debug

            if parent and phone:
                # if not parents.filter(id=parent.id).exists():
                # # if parent not in parents  # and phone.parent == parent and student_id_get == student.id:
                #     messages.error(request, "The selected parent is not registered for this student.")
                if phone.parent_id != parent.id:  # ✅ ensure phone really belongs to that parent
                    messages.error(request, "The selected phone number does not belong to the chosen parent.")
                    return redirect("emrgncy_info")

                elif student_id_get != student.id:
                    messages.error(request, "Selected student does not match the current student on registration.")
                    return redirect("emrgncy_info")
                else:
                    all_exists = EmergencyContact.objects.filter(
                        student=student,
                        parent=parent,
                        phone_num=phone
                    ).exists()
                    if all_exists:
                        messages.warning(request, "This emergency contact is already registered for this student.")
                        return redirect("emrgncy_info")
                    else:
                        emergency = EmergencyContact.objects.create(
                            student=student,
                            parent=parent,
                            phone_num = phone
                            )
                        saved_ids.append(emergency.id)

        if new_form.is_valid():
            emergency = new_form.save(commit=False)
            emergency.student = student

            # prevent duplicates
            exists = EmergencyContact.objects.filter(
                student=student,
                parent=emergency.parent,
                phone_num=emergency.phone_num
            ).exists()
            if exists:
                messages.warning(request, "This new emergency contact is already registered.")
                return redirect("emrgncy_info")
            
            emergency.save()
            saved_ids.append(emergency.id)

        if saved_ids:
            emergency_ids= request.session.get("emergency_ids", [])
            emergency_ids.extend(saved_ids)
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
        new_form = EmergencyContactForm()
        existing_form = ExistingEmergencyContactForm()
        request.session["current_step"] = 4
        request.session.modified = False

    # Display all saved phones for this parent
    # phones = PhoneNumber.objects.filter(parent=parent)
    return render(request, "parents/emergency_enroll.html", {
        "new_form": new_form,
        "existing_form": existing_form,
       }) #"phones": phones})
