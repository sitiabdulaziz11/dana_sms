from django.contrib import admin

# Register your models here.

from .models import Parent, PhoneNumber, EmergencyContact

class ParentAdmin(admin.ModelAdmin):
    """ Parent admin model.
    """
    list_display = (
        'role', 'first_name', 'middle_name', 'last_name', 'age', 'registerd_date'
    )

class PhoneNumberAdmin(admin.ModelAdmin):
    """ Phone number admin model.
    """
    list_display = (
        'parent', 'number', 'owner', 'number_type'
    )

class EmergencyContactAdmin(admin.ModelAdmin):
    """ Phone number admin model.
    """
    list_display = (
        'parent', 'student', 'phone_num'
    )

admin.site.register(Parent, ParentAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(EmergencyContact, EmergencyContactAdmin)
