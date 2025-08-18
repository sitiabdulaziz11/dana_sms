from django.db import models
from django.contrib.auth.models import User
import pycountry

from students.models import StudentRegistration


COUNTRY_CHOICES = sorted([(country.name, country.name) for country in pycountry.countries])


# Create your models here.

class Parent(models.Model):
    """
    Student's Parent Module
    """
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    father_first_name = models.CharField(max_length=100)
    father_middlename = models.CharField(max_length=100)
    father_last_name = models.CharField(max_length=100)
    father_age = models.IntegerField(null=True, blank=True)
    education_level = models.CharField(max_length=100)
    ocupation = models.CharField(max_length=100)
    work_place = models.CharField(max_length=50)
    # father_phone_no = models.IntegerField()
    father_image_file = models.ImageField(null=True, blank=True)
    mother_first_name = models.CharField(max_length=100)
    mother_middlename = models.CharField(max_length=100)
    mother_last_name = models.CharField(max_length=100)
    mother_age = models.IntegerField(null=True, blank=True)
    education_level = models.CharField(max_length=100)
    ocupation = models.CharField(max_length=100)
    work_place = models.CharField(max_length=50)
    # mother_phone_no = models.IntegerField()
    mother_image_file = models.ImageField(null=True, blank=True)
    registration_date = models.DateField(auto_now_add=True)
    city = models.CharField(max_length=50)
    kfle_ketema = models.CharField(max_length=50)
    wereda= models.CharField(max_length=50)
    hous_number = models.CharField(max_length=50)
    nationality = models.CharField(max_length=70, choices=COUNTRY_CHOICES)
    email = models.EmailField(max_length=254, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    


class PhoneNumber(models.Model):
    """Phone number model
    """
    parent = models.ForeignKey('Parent', on_delete=models.CASCADE, related_name='phone_numbers')
    student = models.ForeignKey(StudentRegistration, on_delete=models.SET_NULL, null=True)
    number = models.CharField(max_length=60)
    owner = models.CharField(max_length=30, choices=[('father', 'Father'), ('mother', 'Mother')])
    number_type = models.CharField(max_length=30, choices=[('personal', 'Personal'), ('work phone', 'Work Phone'), ('other', 'Other')])

class EmetgencyContact(models.Model):
    """Emergency contact for a student.
    """
    student = models.ForeignKey(StudentRegistration, on_delete=models.CASCADE, related_name="emergency")
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    registration_date = models.DateField(auto_now_add=True)
    city = models.CharField(max_length=50)
    kfle_ketema = models.CharField(max_length=50)
    wereda= models.CharField(max_length=50)
    hous_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    nationality = models.CharField(max_length=70, blank=True, null=True, choices=COUNTRY_CHOICES)
    signature = models.ImageField(
        upload_to="signatures/",  # folder inside MEDIA_ROOT
        blank=True,
        null=True)
    email = models.EmailField(max_length=254, blank=True, null=True, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True, unique=True)
