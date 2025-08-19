from django.urls import path

from . import views

urlpatterns = [
    path("grade", views.gradeSection_register, name="grade_reg"),
    # path("grade", views.section_register, name="grade_reg"),
    path("success", views.success, name="succes"),
]