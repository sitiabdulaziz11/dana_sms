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
from .forms import PaymentForm
from students.forms import StudentRegistrationForm
from parents.forms import ParentFormSet, PhoneFormSet, EmergencyContactForm

# Create your views here.

def review(request):
    """
    Review and edit all data for a student (student, parents, phones, emergency, payment).
    Uses session['student_id'] instead of pk from URL.
    """
    student_id = request.session.get("student_id")
    if not student_id:
        messages.error(request, "Session expired or student not found. Please restart the registration.")
        return redirect("register")
    student = get_object_or_404(StudentRegistration, pk=student_id)
    parents = student.parents.all()

    try:
        emergency = EmergencyContact.objects.get(student=student)
    except EmergencyContact.DoesNotExist:
       return HttpResponse("No emergency contact")
    try:
        payment = Payment.objects.get(student=student)
    except Payment.DoesNotExist:
       return HttpResponse("No payment")
    
    if request.method == "POST":
        student_form = StudentRegistrationForm(request.POST, request.FILES, instance=student)
        parent_formset = ParentFormSet(request.POST, request.FILES, queryset=parents, prefix="parents")
        emergency_form = EmergencyContactForm(request.POST, request.FILES, instance=emergency)
        payment_form = PaymentForm(request.POST, request.FILES, instance=payment)

        phone_formsets = [
            PhoneFormSet(
                request.POST,
                instance=parent_form.instance,
                prefix=f"phone_{i}",
            )
            for i, parent_form in enumerate(parent_formset.forms)
        ]
        parent_phone_pairs = zip(parent_formset.forms, phone_formsets)

        # Debugging logs
        print("Student form errors:", student_form.errors)
        print("Emergency form errors:", emergency_form.errors)
        print("Parent formset errors:", parent_formset.errors)
        for i, pf in enumerate(phone_formsets):
            print(f"Phone formset {i} errors:", pf.errors)
        print("Payment form errors:", payment_form.errors)

        if (
            student_form.is_valid()
            and emergency_form.is_valid()
            and parent_formset.is_valid()
            and payment_form.is_valid()
            and all(pf.is_valid() for pf in phone_formsets)
        ):
           student_form.save()
           request.session["student_id"] = student.id  # keep in session
           
           parents_saved = parent_formset.save()
           student.parents.set(parents_saved)  # link only these parents
           
           emergency_form.save()
           payment_form.save()
           for pf in phone_formsets:
               pf.save()

           messages.success(request, "All data updated successfully!")
           request.session.pop("parent_ids", None)
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
        emergency_form = EmergencyContactForm(instance=emergency)
        payment_form = PaymentForm(instance=payment)
        for key in ["parent_id", "phone_ids", "student_id"]:
           request.session.pop(key,None)
        request.session.modified = True
        return redirect("success_page")

    return render(
        request,
        "payments/edit_review.html",
        {
            "student_form": student_form,
            "parent_formset": parent_formset,
            "parent_phone_pairs": parent_phone_pairs,
            "emergency_form": emergency_form,
            "payment_form": payment_form,
        },
    )



# def review(request, pk):
#    """ Review and edit all data for a student (student, parents, phones, emergency, payment).
#    """
#    try:
#       student = get_object_or_404(StudentRegistration, pk=pk)
#       print(student)
#       parents = student.parents.all()  # b/c many to many
#       print(parents)
#    except Http404:
#         messages.error(request, "No parent found with that ID.")
#       #   return redirect("?")
#    try:
#       emergency = EmergencyContact.objects.get(student=student)
#    except EmergencyContact.DoesNotExist:
#       # messages.error(request, "No emergency contact found with this student")
#       # return redirect("?")
#       return HttpResponse("No emergency contact")
#    try:
#       payment = Payment.objects.get(student=student)
#    except Payment.DoesNotExist:
#       return HttpResponse("No payment")

      
#    if request.method == "POST":
#       student_form = StudentRegistrationForm(request.POST, request.FILES, instance=student)
#       # parent_formset = ParentFormSet(request.POST, queryset=parents, prefix="parents")
#       parent_formset = ParentFormSet(request.POST, request.FILES, queryset=student.parents.all(), prefix="parents")

#       # parent_formset = ParentFormSet(request.POST, instance=student, prefix="parents")
#       emergency_form = EmergencyContactForm(request.POST, request.FILES, instance=emergency)
#       payment_form = PaymentForm(request.POST, request.FILES, instance=payment)

#       # phone_formsets = [PhoneFormSet(request.POST or None, instance=parent, prefix=f"phone_{parent.id}") for parent in parents]
#       # parent_phone_pairs = zip(parent_formset, phone_formsets)
#       phone_formsets = [PhoneFormSet(request.POST, instance=parent_form.instance, prefix=f"phone_{i}",
#                                      ) for i, parent_form in enumerate(parent_formset.forms)]
#       parent_phone_pairs = zip(parent_formset, phone_formsets)

#       print("Student form errors:", student_form.errors)
#       print("Emergency form errors:", emergency_form.errors)
#       print("Parent formset errors:", parent_formset.errors)
#       for i, pf in enumerate(phone_formsets):
#          print(f"Phone formset {i} errors:", pf.errors)
#       print("Payment form errors:", payment_form.errors)

#       if (student_form.is_valid() and emergency_form.is_valid() and parent_formset.is_valid() and payment_form.is_valid()
#          and all(pf.is_valid() for pf in phone_formsets)):
#          student_form.save()
#          request.session["student"] = student.id

#          # parent_formset.save()
         
#          parents_saved = parent_formset.save()
#          student.parents.set(parents_saved)  # link only these parents
#          # parents = parent_formset.save()
#          # student.parents.set(parents)

#          emergency_form.save()
#          payment_form.save()
#          for pf in phone_formsets:
#             pf.save()

#          messages.success(request, "All data updated successfully!")
#          request.session.pop("parent_ids", None)
#          return redirect("success_page")
#       else:
#             messages.error(request, "Please correct the errors below.")
#    else:
#       parent_formset = ParentFormSet(queryset=student.parents.all(), prefix="parents")
#       student_form = StudentRegistrationForm(instance=student)
#       # parent_formset = ParentFormSet(queryset=parents)
#       # parent_formset = ParentFormSet(instance=student, prefix="parents")
#       # phone_formsets = [PhoneFormSet(instance=parent, prefix=f"phone_{parent.id}") for parent in parents]

#       phone_formsets = [
#             PhoneFormSet(
#                 instance=parent_form.instance,
#                 prefix=f"phone_{i}",
#             )
#             for i, parent_form in enumerate(parent_formset.forms)
#         ]
#       parent_phone_pairs = zip(parent_formset.forms, phone_formsets)
#       emergency_form = EmergencyContactForm( instance=emergency)
#       payment_form = PaymentForm(instance=payment)
#       return redirect("success_page")


   
#    return render(request, "payments/edit_review.html", {
#       "student_form": student_form,
#       "parent_formset": parent_formset,
#       "parent_phone_pairs": parent_phone_pairs,
#       "emergency_form": emergency_form,
#       "payment_form": payment_form,
#    })


"""
From Student → Parent (1 side)
student = Student.objects.get(id=1)
parent = student.parent   # single Parent object

From Parent → Students (many side)
parent = Parent.objects.get(id=1)
students = parent.students.all()   # queryset of Student objects"""

def make_payment(request, student_id=None):
   """views to make student payment.
   """
   student = None

   if student_id:
      try:
         student = StudentRegistration.objects.get(id=student_id)
      except StudentRegistration.DoesNotExist:
         # return HttpResponse("Sorry, no student exists")
         return render(request, "payments/student_not_found.html", {
            "student_id": student_id
         })
      
   payment_form = PaymentForm(request.POST or None, request.FILES or None)
   if request.method == "POST" and student:
      # payment_form = PaymentForm(request.POST, request.FILES)
      if payment_form.is_valid():
         try:
            payment = payment_form.save(commit=False)
            payment.student = student
            payment.save()
            request.session["payment_id"] = payment.id
            messages.success(request, "Payment success")
            # return redirect("review")
            # return redirect("edit", pk=student_id)
            return redirect("edit")
         except ValidationError:
            messages.error(request, "⚠️ Duplicate payment: This student already paid for this month and type.")
            return redirect("pay", student_id=student_id)
   else:
      payment_form = PaymentForm()
      request.session["current_step"] = 5
      request.session.modified = False
      
   return render(request, "payments/make_payment.html", {
      "form": payment_form,
      "student": student,
   })

def review_all_enrollment(request):
   """ Review all entered information before final submission.
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
   
   parent = Parent.objects.filter(id__in=parent_ids)  #? what this filter?

   all_phone_ids = []
   for p_phones in phone_ids.values():
      all_phone_ids.extend(p_phones)
   phones = PhoneNumber.objects.filter(id__in=all_phone_ids)

   emergencies = EmergencyContact.objects.filter(id__in=emergency_ids)
   student = StudentRegistration.objects.get(id=student_id)
   # student = get_object_or_404(StudentRegistration, id=student_id)
   #  parents = student.parents.all()  # # all parents linked to this student
   payment = Payment.objects.get(id=payment_id)

   if request.method == "POST":
      # clear review_mode after final submit
      request.session.pop("review_mode", None)
      request.session.pop("student_id", None)
      request.session.pop("parent_ids", None)
      request.session.pop("phone_ids", None)
      request.session.pop("emergency_ids", None)
      return redirect("success_page")
   
   return render(request, "payments/review_all.html", {
      "parents": parent,
      "phones": phones,
      "emergencies": emergencies,
      "student": student,
      "payment": payment
   })



def payment_success(request):
   """To handle successful request.
   """
   return render(request, "payment/success.html")
