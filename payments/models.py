from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from students.models import StudentRegistration

# Create your models here.

PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
    ]


class Payment(models.Model):
    """Model which handles payment status.
    """
    MONTH_CHOICES = [
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
    
    PAYMENT_TYPE_CHOICES = [
        ('registration', 'Registration'),
        ('monthly', 'Monthly'),
        ('after_class', 'After Class Reading'),
    ]
    
    # Relation with student model 
    student = models.ForeignKey(StudentRegistration, on_delete=models.CASCADE, related_name='payments')

    amount = models.FloatField()
    debited_month = models.CharField(max_length=120, choices=MONTH_CHOICES, blank=True, null=True)
    payment_type = models.CharField(max_length=120, choices=PAYMENT_TYPE_CHOICES, null=True, blank=True)  # monthly or for after class redding
    payment_status = models.CharField(max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        blank=True,
        null=True)  # payid or not payid
    payer_name = models.CharField(max_length=120, null=True, blank=True)   #?
    payment_receipt_image = models.ImageField(upload_to="receipts/", null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    #  payer name need or not student is enough or?

    debited_date_time = models.DateTimeField(default=timezone.now)
    # debited_date = models.DateField(auto_now_add=True)

    class Meta:
        """To make sure the same student can't pay twice for the same month and type.
        """
        unique_together = ('student', 'debited_month', 'payment_type')
        ordering = ['-debited_date_time']
    
    # def clean(self):
    #     """Custom validation logic
    #     """
    #     if self.payment_type == 'registration':
    #         # self.payment_status = None
    #         self.debited_month = None
    #     else:
    #         if not self.debited_month:
    #             raise ValidationError("debited_month is required.")
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Calls the clean() method before saving
        
        # if not self.debited_date_time:
        #     self.payment_status = 'pending'
        # self.payment_status = 'paid'

        super().save(*args, **kwargs)


    def __str__(self):
        return f"  {self.student} - {self.debited_month} - {self.payment_type} - {self.payment_status} - {self.amount} - {self.debited_date_time} - {self.payer_name}"
