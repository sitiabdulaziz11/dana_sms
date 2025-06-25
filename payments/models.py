from django.db import models

# Create your models here.

class Payment(models.Model):
    """Model which handles payment status.
    """
    payer_name = models.CharField(max_length=120)
    amount = models.FloatField()
    debited_date = models.DateField(auto_now_add=True)
    debited_month = models.CharField(max_length=50)
    payment_type= models.CharField()  # monthly or for redding
    payment_status = models.CharField()  # payid or not payid

    # Relation with Payment model
student = models.ForeignKey('StudentRegistration', on_delete=models.CASCADE, related_name='payments')

