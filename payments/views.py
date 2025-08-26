# import os
import uuid
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import Http404, HttpResponse



from .models import Payment
# from .models import MONTH_CHOICES
from students.models import StudentRegistration
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
         # return redirect("succes")
   else:
      payment_form = PaymentForm()
   return render(request, "payments/make_payment.html", {
      "form": payment_form,
      "student": student
   })


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
