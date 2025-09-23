from django.urls import path
from . import views
from .views import ParentEnrollmentWizard, FORMS

urlpatterns = [
    path("parent", views.parent_info, name="prnt_info"),
    path("phone", views.phoneNum_info, name="phone_info"),
    path("emergency", views.emergency_info, name="emrgncy_info"),
    path("wizard/", ParentEnrollmentWizard.as_view(FORMS), name="wizard"),
]
