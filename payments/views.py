import uuid
import requests
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import Http404, HttpResponse

from .models import Payment
# from .models import MONTH_CHOICES
from students.models import StudentRegistration
from parents.models import Parent, PhoneNumber, EmergencyContact
from .forms import PaymentForm, PaymentFormSet
from students.forms import StudentRegistrationForm
from parents.forms import ParentFormSet, PhoneFormSet, EmergencyContactForm, EmergencyContactFormSet

# Create your views here.


def make_payment(request, student_id=None):
   """views to make student payment.
   """
   student = None

   if student_id:
      try:
         student = StudentRegistration.objects.get(id=student_id)
      except StudentRegistration.DoesNotExist:
         messages.error(request,"Sorry, no student exists")
         return redirect("register")
      
   payment_form = PaymentForm(request.POST or None, request.FILES or None)
   if request.method == "POST" and student:
      if payment_form.is_valid():
         try:
            payment = payment_form.save(commit=False)
            payment.student = student
            payment.save()
            request.session["payment_id"] = payment.id
            messages.success(request, "Payment success")
            # return redirect("review")          

            if "add_another" in request.POST:
               #  return redirect("pay", student_id=student_id)
                return redirect("pay_with_id", student_id=student.id)
            
            request.session.pop("current_step", None)
            return redirect("edit")
         
         except ValidationError:
            messages.error(request, "⚠️ Duplicate payment: This student already paid for this month and type.")
            return redirect("pay_with_id", student_id=student_id)
   else:
      payment_form = PaymentForm()
      request.session["current_step"] = 5
      request.session.modified = False
      
   return render(request, "payments/make_payment.html", {
      "form": payment_form,
      "student": student,
   })


def review_all(request):
   """ To review and edit all entered information before final submission.
   """
   request.session["review_mode"] = True  # mark review mode

   parent_ids = request.session.get("parent_ids", [])
   phone_ids = request.session.get("phone_ids", [])
   emergency_ids = request.session.get("emergency_ids", [] )
   student_id = request.session.get("student_id")
   payment_id = request.session.get("payment_id")

   if not parent_ids:
      print("SESSION parent_ids:", request.session.get("parent_ids"))  #?
      messages.error(request, "No parent ID provided.")
      # request.session["review_mode"] = True
      return redirect("prnt_info")
   if not phone_ids:
      messages.error(request, "No phone ID provided.")  #for what dad or mom? add that logic
      return redirect("phone_info")
   if not emergency_ids:
      messages.error(request, "No emergency ID provided.")
      return redirect("emrgncy_info")
   if not student_id:
      messages.error(request, "No student ID provided.")
      return redirect("register")
   if not payment_id:
      messages.error(request, "No payment ID provided.")
      return redirect("pay_with_id", student_id)
   
   parents = Parent.objects.filter(id__in=parent_ids)  #? what this filter?

   emergency = EmergencyContact.objects.filter(id__in=emergency_ids)
   student = StudentRegistration.objects.get(id=student_id)
   # student = get_object_or_404(StudentRegistration, id=student_id)
   #  parents = student.parents.all()  # # all parents linked to this student
   payments = Payment.objects.filter(id=payment_id)

   if request.method == "POST":
      student_form = StudentRegistrationForm(request.POST, request.FILES, instance=student)
      parent_formset = ParentFormSet(request.POST, request.FILES, queryset=parents, prefix="parents")
      emergency_formset = EmergencyContactFormSet(request.POST, request.FILES, queryset=emergency, prefix="Emergency")
      payment_formset = PaymentFormSet(request.POST, request.FILES, queryset=payments, prefix="Payments")
      phone_formsets = [
            PhoneFormSet(
                request.POST,
                instance=parent_form.instance,
                prefix=f"phone_{i}",
            )
            for i, parent_form in enumerate(parent_formset.forms)
        ]
      parent_phone_pairs = zip(parent_formset.forms, phone_formsets)
      
      if(
         student_form.is_valid()
         and emergency_formset.is_valid()
         and parent_formset.is_valid()
         and payment_formset.is_valid()
         and all(pf.is_valid() for pf in phone_formsets)
        ):
        student_form.save()
           
        parents_saved = parent_formset.save()
        student.parents.set(parents_saved)  # link only these parents
           
        emergency_formset.save()
        payment_formset.save()
        for pf in phone_formsets:
         pf.save()

         messages.success(request, "All data registered successfully!")
         request.session.pop("review_mode", None)
         request.session.pop("student_id", None)
         request.session.pop("parent_ids", None)
         request.session.pop("phone_ids", None)
         request.session.pop("emergency_ids", None)
         return redirect("success_page")
        
        else:
         messages.error(request, "Please correct the errors below.")
   else:  # GET
      student_form = StudentRegistrationForm(instance=student)
      parent_formset = ParentFormSet(queryset=parents, prefix="parents")
      phone_formsets = [
         PhoneFormSet(
               instance=parent_form.instance,
               prefix=f"phone_{i}",
         )
         for i, parent_form in enumerate(parent_formset.forms)
      ]

      parent_phone_pairs = zip(parent_formset.forms, phone_formsets)
      emergency_formset = EmergencyContactFormSet(queryset=emergency, prefix="Emergency")
      payment_formset = PaymentFormSet(queryset=payments, prefix="Payments")


   return render(
      request,
      "payments/edit_review.html",
      {
         "student_form": student_form,
         "parent_formset": parent_formset,
         "parent_phone_pairs": parent_phone_pairs,
         "emergency_formset": emergency_formset,
         "payment_formset": payment_formset,
      },
   )
      


def review(request):
    """
    Review and edit all data for a student (student, parents, phones, emergency, payment).
    """
    student_id = request.session.get("student_id")
    parent_ids = request.session.get("parent_ids", [])
    phone_ids = request.session.get("phone_ids", [])
    emergency_ids = request.session.get("emergency_ids", [] )
    payment_id = request.session.get("payment_id")
    
    if not student_id:
        messages.error(request, "Session expired or student not found. Please select from the list oor restart the registration.") # how to make to select?
        return redirect("register")
    
    student = get_object_or_404(StudentRegistration, pk=student_id)
    parents = student.parents.all()
    print(parents)  # debug
    
    emergency = EmergencyContact.objects.filter(student=student)

   
      #   payment = Payment.objects.get(student=student
    payments = Payment.objects.filter(student=student)
    if not payments.exists():
      return HttpResponse("No payment record found for this student.")
    
    if request.method == "POST":
        student_form = StudentRegistrationForm(request.POST, request.FILES, instance=student)
        parent_formset = ParentFormSet(request.POST, request.FILES, queryset=parents, prefix="parents")
        emergency_formset = EmergencyContactFormSet(request.POST, request.FILES, queryset=emergency, prefix="Emergency")
      #   payment_form = PaymentForm(request.POST, request.FILES, instance=payment)
        payment_formset = PaymentFormSet(request.POST, request.FILES, queryset=payments, prefix="Payments")

        phone_formsets = [PhoneFormSet(request.POST or None, instance=parent, prefix=f"phone_{parent.id}") for parent in parents]

        parent_phone_pairs = zip(parent_formset.forms, phone_formsets)

        # Debugging logs
        print("Student form errors:", student_form.errors)
        print("Emergency form errors:", emergency_formset.errors)
        print("Parent formset errors:", parent_formset.errors)
        for i, pf in enumerate(phone_formsets):
            print(f"Phone formset {i} errors:", pf.errors)
        print("Payment form errors:", payment_formset.errors)

        if (
            student_form.is_valid()
            and emergency_formset.is_valid()
            and parent_formset.is_valid()
            and payment_formset.is_valid()
            and all(pf.is_valid() for pf in phone_formsets)
        ):
           student_form.save()
           parent_formset.save()
           
           emergency_formset.save()
           payment_formset.save()
           for pf in phone_formsets:
               pf.save()

           messages.success(request, "All Data Saved successfully!")
           request.session.pop("parent_ids", None)
           request.session.pop("phone_ids", None)
           request.session.pop("emergency_ids", None)
           return redirect("success_page")
        else:
            messages.error(request, "Please correct the errors below.")

    else:  # GET
        student_form = StudentRegistrationForm(instance=student)
        parent_formset = ParentFormSet(queryset=parents, prefix="parents")

        phone_formsets = [PhoneFormSet(request.POST or None, instance=parent, prefix=f"phone_{parent.id}") for parent in parents]

        parent_phone_pairs = zip(parent_formset.forms, phone_formsets)
        emergency_formset = EmergencyContactFormSet(queryset=emergency, prefix="Emergency")
        payment_formset = PaymentFormSet(queryset=payments, prefix="Payments")

    return render(
        request,
        "payments/edit_review.html",
        {
            "student_form": student_form,
            "parent_formset": parent_formset,
            "parent_phone_pairs": parent_phone_pairs,
            "emergency_formset": emergency_formset,
            "payment_formset": payment_formset,
        },
    )


def payment_success(request):
   """To handle successful request.
   """
   return render(request, "payment/success.html")
