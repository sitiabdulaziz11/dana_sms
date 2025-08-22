from django.urls import path

# from .views import initialize_payment
from . import views


urlpatterns = [
    path("payment/<int:student_id>/", views.make_payment, name="pay"),
    # path('init/<int:student_id>', views.initialize_payment, name='init_pay'),
    # path("payment/verify/", views.verify_payment, name="verify_payment"),
    # path("payment/success/", views.payment_success, name="payment_success")
]