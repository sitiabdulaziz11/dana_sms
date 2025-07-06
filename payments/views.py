from django.shortcuts import render

from .models import Payment
from .models import MONTH_CHOICES

# Create your views here.










def unpaid_monthly_payments(request):
    """To display unpaid and number of unpaid srudents.
    """
    payments = Payment.objects.filter(payment_type='monthly', payment_status='pending')

    unpaid_counts = {}
    for month in MONTH_CHOICES:
        unpaid_count = Payment.objects.filter(
            debited_month=month,
            payment_type='monthly',
            payment_status='pending'
        ).count()
        unpaid_counts[month] = unpaid_count

    return render(request, 'payment_list.html', {
        'payments': payments,
        'unpaid_counts': unpaid_counts
        })
