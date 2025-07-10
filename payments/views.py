from django.shortcuts import render

# from .models import Payment
# from .models import MONTH_CHOICES
from django.http import Http404
from .models import StudentRegistration

# Create your views here.

def student_payment_history(request, stud_id):
   """Function which display students payment history
   """
   try:
     student = StudentRegistration.objects.get(id=stud_id)
   except StudentRegistration.DoesNotExist:
      raise Http404("Student not found.")
   
   all_payments = student.payments.all()   # to get all payments
   monthly_payments = all_payments.filter(paymen_type="monthly")

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
