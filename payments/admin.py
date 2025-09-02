from django.contrib import admin

from .models import Payment

# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    """To customise Payment admin
    """
    list_filter = ("payment_status", "payment_type", "debited_month", )
    readonly_fields = ("payment_status",)  # not to edit manualy
    # list_display = ('student',  'amount',  'debited_month', 'payment_type','payment_status', 'payer_name', 'debited_date_time',)
    list_display = [field.name for field in Payment._meta.get_fields()
                    if field.concrete and not field.many_to_many]



admin.site.register(Payment, PaymentAdmin)
