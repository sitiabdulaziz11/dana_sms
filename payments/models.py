from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

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
    debited_date_time = models.DateTimeField(default=timezone.now)
    # debited_date = models.DateField(auto_now_add=True)
    debited_month = models.CharField(max_length=120, choices=MONTH_CHOICES)
    payment_type = models.CharField(max_length=120, choices=PAYMENT_TYPE_CHOICES,
        blank=True,
        null=True )  # monthly or for after class redding
    payment_status = models.CharField(max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        blank=True,
        null=True)  # payid or not payid
 
    # Relation with student model 
    student = models.ForeignKey(StudentRegistration, on_delete=models.CASCADE, related_name='payments') #  payer name need or not student is enough or?

    class Meta:
        """To make sure the same student can't pay twice for the same month and type.
        """
        unique_together = ('student', 'debited_month', 'payment_type')
        ordering = ['-debited_date_time']
    
    def clean(self):
        """Custom validation logic
        """
        if self.debited_month == 'Registration':
            self.payment_status = None
            self.payment_type = None
        else:
            if not self.payment_status or not self.payment_type:
                raise ValidationError("Payment type and status are required unless it's Registration.")
    
    # def save(self, *args, **kwargs):
    #     self.full_clean()  # Calls the clean() method before saving
    #     super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.payer_name} - {self.student} - {self.debited_month} - {self.payment_type} - {self.payment_status} - {self.debited_date_time}"
