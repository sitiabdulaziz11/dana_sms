from django.db import models
from django.contrib.auth.models import User
import pycountry
from datetime import datetime

from parents.models import Parent

# Create your models here.

gender_choice = [
    ('male', 'Male'),
    ('female','Female'),
    ('other', 'Other'),
]

COUNTRY_CHOICES = sorted([(country.name, country.name) for country in pycountry.countries])


class StudentRegistration(models.Model):
    """Studentes information.
    """
    # user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=15, choices=gender_choice)
    # email = models.EmailField(max_length=254, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    age = models.IntegerField()
    image_file = models.ImageField()
    address = models.CharField(max_length=60)
    registration_date = models.DateField(auto_now_add=True)
    kebele_wereda = models.CharField(max_length=50)
    kfleketema = models.CharField(max_length=50)
    hous_number = models.CharField(max_length=50)
    nationality = models.CharField(max_length=70, choices=COUNTRY_CHOICES)
    join_year = models.CharField(max_length=2)

    # Relations
    # parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    # phone_no from parent or? grade, section other separet table or?, email , password good or?
    # result, teachers, subjects, admin and parent.

    class Meta:
        """Meta class to custemize student registration class.
        """
        ordering = ['first_name']
    
    def custom_id(self):
        """To customize id
        """
        return f"A/D/{self.id}/{self.join_year}"
    
    def save(self, *args, **kwargs):
        if not self.join_year:
            self.join_year = str(datetime.now().year)[-2]
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.first_name} {self.middlename} {self.last_name}"
