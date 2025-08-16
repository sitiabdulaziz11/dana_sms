from django.urls import path

from . import views


urlpatterns = [
    path("", views.main_page, name="main"),
    path("dashboards", views.dashboards, name="dashboard"),
]