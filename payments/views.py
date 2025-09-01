# import os
import uuid
import requests
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import Http404, HttpResponse



from .models import Payment
# from .models import MONTH_CHOICES
from students.models import StudentRegistration
from parents.models import Parent, PhoneNumber, EmergencyContact
from .forms import PaymentForm

# Create your views here.

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
         payment = payment_form.save(commit=False)
         payment.student = student
         payment.save()
         request.session["payment_id"] = payment.id
         messages.success(request, "Payment success")
         return redirect("review")
   else:
      payment_form = PaymentForm()
   return render(request, "payments/make_payment.html", {
      "form": payment_form,
      "student": student
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

   # Ensure it's always iterable
   # if isinstance(parent_ids, int):
   #  parent_ids = [parent_ids]

   if not parent_ids:
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
   
   parent = Parent.objects.filter(id__in=parent_ids)

   all_phone_ids = []
   for p_phones in phone_ids.values():
      all_phone_ids.extend(p_phones)
   phones = PhoneNumber.objects.filter(id__in=all_phone_ids)

   emergencies = EmergencyContact.objects.filter(id__in=emergency_ids)
   student = StudentRegistration.objects.get(id=student_id)
   payment = Payment.objects.get(id=payment_id)

   if request.method == "POST":
      # clear review_mode after final submit
      request.session.pop("review_mode", None)
      return redirect("success_page")
   
   return render(request, "payments/review_all.html", {
      "parents": parent,
      "phones": phones,
      "emergencies": emergencies,
      "student": student,
      "payment": payment
   })

# required_steps = {
#       "parent_id": ("prnt_info", "No parent ID provided."),
#       "phone_id": ("phone_info", "No phone ID provided."),
#       "emergency_id": ("emrgncy_info", "No emergency ID provided."),
#       "student_id": ("register", "No student ID provided."),
#       "payment_id": ("prnt_info", "No payment ID provided."),
#    }

   # for key, (redirect_url, error_message) in required_steps.items():
   #    if not request.session.get(key):
   #       messages.error(request, error_message)
   #       return redirect(redirect_url)
   # return render(request, "payments/review.html", {
   #    "required_sp": required_steps
   # })



# def initialize_payment(request, student_id):
#    """To initialize payment.
#    """
#    student = StudentRegistration.objects.get(id=student_id)

#    tx_ref = f"schoolfee_{uuid.uuid4()}"   # str(uuid.uuid4())?
#    # tx_ref = f"schoolfee_{student.id}_{uuid.uuid4()}" ?
#    chapa_url = "https://api.chapa.co/v1/transaction/initialize"   #? what is it and how i get it?
#    chapa_secret = settings.CHAPA_SECRET_KEY

#    headers = {
#       # "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
#       "Authorization": f"Bearer {chapa_secret}",
#    }   #?

#    latest_payment = student.payments.last()

#    if latest_payment:
#       data = {
#       "amount": str(latest_payment.amount),
#       "currency": "ETB",
#       "email": student.Payment.email,  # ?
#       "first_name": student.first_name,  # ?
#       "middle_name": student.middle_name,
#       "tx_ref": tx_ref,
#       "callback_url": "http://127.0.0.1:8000/payment/verify/",
#       "return_url": "http://127.0.0.1:8000/payment/success/",
#       "customization": {
#          "title": "School Fee Payment",
#          "description": f"Payment for {student.first_name}",
#       }
#    }

#    response = requests.post(chapa_url, json=data, headers=headers)  #?
#    if response.status_code == 200:
#       payment_url = response.json()["data"]["checkout_url"]
#       return redirect(payment_url)
#    else:
#       print(response.json())   # for debugging
#       redirect("/payment/error")
#       # return HttpResponse("Error initiating payment")

# def verify_payment(request):
#    """Callback route to verify payment after processing on Chapa.
#    """
#    tx_refc = request.GET.get("tx_ref")

#    if not tx_refc:
#       return HttpResponse("Transaction reference not found", status=400)
   
#    url = f"https://api.chapa.co/v1/transaction/verify/{tx_refc}"
#    headers={"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}

#    response = requests.get(url, headers=headers)

#    if response.status_code == 200:
#       data = response.json()
#       if data["status"] == "success":
#          # Update payment status in DB
#          return redirect("payment_success")
#    return redirect("payment_error")


def payment_success(request):
   """To handle successful request.
   """
   return render(request, "payment/success.html")



# def student_payment_history(request, stud_id):
#    """Function which display students payment history
#    """
#    try:
#      student = StudentRegistration.objects.get(id=stud_id)
#    except StudentRegistration.DoesNotExist:
#       raise Http404("Student not found.")
   
#    all_payments = student.payments.all()   # to get all payments
#    monthly_payments = all_payments.filter(paymen_type="monthly")

   # # 🔁 Get monthly payment for each month
   # monthly_by_month = {}
   # for month, label in MONTH_CHOICES:
   #      monthly_by_month[month] = monthly_payments.filter(debited_month=month).first()

   #  context = {
   #      "student": student,
   #      "all_payments": all_payments,
   #      "monthly_payments": monthly_payments,
   #      "monthly_by_month": monthly_by_month,
   #  }

   #  return render(request, "your_template.html", context)


# def unpaid_monthly_payments(request):
#     """To display unpaid and number of unpaid srudents.
#     """
#     payments = Payment.objects.filter(payment_type='monthly', payment_status='pending')

#     unpaid_counts = {}
#     for month in MONTH_CHOICES:
#         unpaid_count = Payment.objects.filter(
#             debited_month=month,
#             payment_type='monthly',
#             payment_status='pending'
#         ).count()
#         unpaid_counts[month] = unpaid_count

#     return render(request, 'payment_list.html', {
#         'payments': payments,
#         'unpaid_counts': unpaid_counts
#         })


# from django.shortcuts import get_object_or_404, redirect
# from django.views.decorators.http import require_POST
# from .models import Payment

# @require_POST
# def mark_payment_paid(request, payment_id):
#     payment = get_object_or_404(Payment, id=payment_id)
#     payment.payment_status = "paid"
#     payment.save()
#     return redirect("payment_history", student_id=payment.student.id)
