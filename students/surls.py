from django.urls import path

from . import views


urlpatterns = [
    path("", views.main_page, name="main"),
    path("dashboards", views.dashboards, name="dashboard"),
    path("student", views.register_student, name="register"),
    path("success", views.success, name="success_page"),
    path("academy", views.academicYear_register, name="A_year"),
    
]