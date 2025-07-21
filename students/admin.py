from django.contrib import admin

from .models import StudentRegistration
from payments.models import Payment

# Register your models here.

    
class PaymentMonthFilter(admin.SimpleListFilter):
    """ Filter by month (from related payment model)
    """
    title = 'Monthly payment'
    parameter_name = 'month'

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
            paid_students_ids = Payment.objects.filter(debited_month=self.value(), payment_status='').values_list('student_id', flat=True)
            if self.value() == 'paid':
                return queryset.filter(id__in=paid_students_ids)
            return queryset.exclude(id__in=paid_students_ids)
        return queryset
    
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
        month = request.GET.get('month')
        payment_type = request.GET.get('payment_type')

        filter_kwargs = {}
        if month:
            filter_kwargs['debited_month'] = month
        if payment_type:
            filter_kwargs['payment_type'] = payment_type
        
        paid_students_ids = Payment.objects.filter(**filter_kwargs, payment_status='paid').values_list('student_id', flat=True)
        if self.value() == 'paid':
            return queryset.filter(id__in=paid_students_ids)
        elif self.value() == 'pending':
            return queryset.exclude(id__in=paid_students_ids)
        return queryset

class PaymentTypeFilter(admin.SimpleListFilter):
    """To filter by payment type.
    """
    title = 'Payment Type'
    parameter_name = 'payment_type'

    def lookups(self, request, model_admin):
        return Payment.PAYMENT_TYPE_CHOICES
    
    def queryset(self, request, queryset):
        return queryset

class StudentRegistrationAdmin(admin.ModelAdmin):
    """To update student registration model.
    """
    list_filter = (PaymentStatusFilter, PaymentMonthFilter, PaymentTypeFilter,)
    

admin.site.register(StudentRegistration, StudentRegistrationAdmin)
