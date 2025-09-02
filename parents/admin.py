from django.contrib import admin

# Register your models here.

from students.models import StudentRegistration
from .models import Parent, PhoneNumber, EmergencyContact

class ParentAdmin(admin.ModelAdmin):
    """ Parent admin model.
    """
    list_display = [field.name for field in Parent._meta.get_fields()
                    if field.concrete and not field.many_to_many]

class ParentInline(admin.TabularInline):
    model = StudentRegistration.parents.through  # for many-to-many
    extra = 1


class PhoneNumberAdmin(admin.ModelAdmin):
    """ Phone number admin model.
    """
    list_display = [field.name for field in PhoneNumber._meta.get_fields()
                    if field.concrete and not field.many_to_many]

class EmergencyContactAdmin(admin.ModelAdmin):
    """ Phone number admin model.
    """
    list_display = [field.name for field in EmergencyContact._meta.get_fields()
                    if field.concrete and not field.many_to_many]

    # list_display = (
    #     'parent', 'student', 'phone_num'
    # )

admin.site.register(Parent, ParentAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(EmergencyContact, EmergencyContactAdmin)
