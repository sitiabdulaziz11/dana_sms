from django.contrib import admin

from .models import StudentRegistration, Enrollment
from payments.models import Payment
from parents.admin import ParentInline

# Register your models here.

    
class PaymentMonthFilter(admin.SimpleListFilter):
    """ Filter by month (from related payment model)
    """
    title = 'Monthly payment'
    parameter_name = 'month'

    def lookups(self, request, model_admin):
        """Define dropdown filter options in admin
        """
        raw_months = Payment.objects.values_list('debited_month', flat=True)  #.distinct()  # To get distinct months from Payment model.
        cleaned_months = set(month.strip().capitalize() for month in raw_months if month)
        return [(month, month) for month in cleaned_months if month]
        # return [(month, month) for month in sorted(cleaned_months) if month] # sorted used to ordedr alphabeticaly
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
    list_filter = (PaymentStatusFilter, PaymentTypeFilter, PaymentMonthFilter, )
    list_display = (
        'custom_id', 'first_name', 'middle_name', 'last_name', 'get_parents', 'get_parent_ids',
        'gender', 'age', 'grade', 'section', 'registration_date', 'city', 'kfle_ketema', 'wereda', 'hous_number', 'image_file', 'birth_date','nationality', 'email', 'password', 'join_year'
    )
    list_display_links = ('custom_id',)
    search_fields = ('first_name', 'last_name',)
    inlines = [ParentInline]   #  to edit related objects (like Parents) directly inside the Student form

    def get_parent_ids(self, obj):
        """ To get parent id on student table.
        """
        return ", ".join(str(p.id) for p in obj.parents.all())
    get_parent_ids.short_description = "Parent ids"

    def get_parents(self, obj):
        """ To get both parents of a student.
        """
        # return ", ".join([str(parent.first_name + " " + parent.last_name) for parent in obj.parents.all()])

        return ", ".join(
            f"{parent.first_name or ''} {parent.middle_name or ''} {parent.last_name or ''}".strip()
            for parent in obj.parents.all())
    
    get_parents.short_description = "parents"
    
    def custom_id(self, obj):
        """ To coustomize student id.
        """
        # return f"A/D/{obj.id}/25"
        return obj.custom_id()
    custom_id.short_description = "Student ID"

class EnrollmentAdmin(admin.ModelAdmin):
    """models for enrollment 
    """
    list_display = ["student", "grade", "section", "academic_year", "enrollment_date"]

admin.site.register(StudentRegistration, StudentRegistrationAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
