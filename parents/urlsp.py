from django.urls import path
from . import views

urlpatterns = [
    path("enroll/parent", views.parent_info, name="prnt_info"),
    path("enroll/phone", views.phoneNum_info, name="phone_info"),
    path("enroll/emergency", views.emergency_info, name="emrgncy_info"),
]
