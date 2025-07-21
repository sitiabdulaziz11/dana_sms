from django.contrib import admin

from .models import Payment

# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    """To customise Payment admin
    """
    list_filter = ("payment_status", "payment_type", "debited_month", )
    readonly_fields = ("payment_status",)  # not to edit manualy


admin.site.register(Payment, PaymentAdmin)
