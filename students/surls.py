from django.urls import path, include

from . import views


urlpatterns = [
    path("", views.main_page, name="main"),
    path("dashboards/", views.dashboards, name="dashboard"),
    path("student", views.register_student, name="register"),
    path("success", views.success, name="success_page"),
    path("academy", views.academicYear_register, name="A_year"),
    
    # path("login", views.login_page, name="login"),
    path("log_out", views.logout_page, name="log_out"),
    path("accounts/profile/", views.profile_page, name="profile"),
    
    # path("accounts/", include("django.contrib.auth.urls")),
    
]