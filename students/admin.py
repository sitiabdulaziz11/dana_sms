from django.contrib import admin

from .models import StudentRegistration
from payments.models import Payment

# Register your models here.

class PaymentStatusFilter(admin.SimpleListFilter):
    """
    """
    title = 'payment Status'
    parameter_name = 'payment_status'

    def lookups(self, request, model_admin):
        return (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        )
    
    def queryset(self, request, queryset):
        """
        """
        if self.value() == 'paid':
            # Get student IDs that have at least one paid payment
            # paid_ids = Payment.objects.filter(payments__payment_status='paid').values_list('student_id', flat=True)
            # return queryset.filter(id__in=paid_ids)
            return queryset.filter(payments__payment_status='paid')
        elif self.value() == 'pending':
            # pending_ids = Payment.objects.filter(payments__payment_status='pending').values_list('student_id', flat=True)
            # return queryset.filter(id__in=pending_ids)
            return queryset.exclude(payments__payment_status='paid')
        return queryset
    
class PaymentMonthFilter(admin.SimpleListFilter):
    """ Filter by month (from related payment model)
    """
    title = 'Monthly payment'
    parameter_name = 'debited_month'

    def lookups(self, request, model_admin):
        """Define dropdown filter options in admin
        """
        months = Payment.objects.values_list('debited_month', flat=True).distinct()  # To get distinct months from Payment model.
        return [(month, month) for month in months if month]
        # return Payment.MONTH_CHOICES
    
    def queryset(self, request, queryset):
        """Actually filter records based on selected value.
        """
        if self.value():
            paid_students_ids = Payment.objects.filter(debited_month=self.value(), payment_status='paid').values_list('student_id', flat=True)
            if self.value() == 'paid':
                return queryset.filter(id__in=paid_students_ids)
            return queryset.exclude(id__in=paid_students_ids)
            # return queryset.filter(payments__debited_month=self.value())
        return queryset


class StudentRegistrationAdmin(admin.ModelAdmin):
    """To update student registration model.
    """
    list_filter = (PaymentStatusFilter, PaymentMonthFilter,)
    

admin.site.register(StudentRegistration, StudentRegistrationAdmin)
