from django.db import models

from students.models import StudentRegistration

# Create your models here.

MONTH_CHOICES = [
    ('Registration', 'Registration'),
    ('September', 'Meskerem/September'),
    ('October', 'Tqmt/October'),
    ('November', 'Hdar/November'),
    ('December', 'Tehsas/December'),
    ('January', 'Tr/January'),
    ('February', 'Yekatit/February'),
    ('March', 'Megabit/March'),
    ('April', 'Miyaziya/April'),
    ('May', 'Gnbot/May'),
    ('June', 'Sene/June'),
]
PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
    ]

PAYMENT_TYPE_CHOICES = [
        ('monthly', 'Monthly'),
        ('after_class', 'After Class Reading'),
    ]


class Payment(models.Model):
    """Model which handles payment status.
    """
    payer_name = models.CharField(max_length=120)   #?
    amount = models.FloatField()
    debited_date = models.DateField(auto_now_add=True)
    debited_month = models.CharField(max_length=120, choices=MONTH_CHOICES)
    payment_type= models.CharField(max_length=120, choices=PAYMENT_TYPE_CHOICES )  # monthly or for after class redding
    payment_status = models.CharField(max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending')  # payid or not payid
 
    # Relation with student model 
    student = models.ForeignKey(StudentRegistration, on_delete=models.CASCADE, related_name='payments') #  payer name need or not student is enough or?

    def __str__(self):
        return f"{self.payer_name} - {self.student} - {self.debited_month} - {self.payment_type} - {self.payment_status} - {self.debited_date}"
