from django.db import models
from django.contrib.auth.models import User
import pycountry
from django.utils import timezone

from students.models import StudentRegistration


COUNTRY_CHOICES = sorted([(country.name, country.name) for country in pycountry.countries])


# Create your models here.

RELATION_CHOICES = [
    ('father', 'Father'),
    ('mother', 'Mother'),
    ('guardian', 'Guardian'),
    ('uncle', 'Uncle'),
    ('aunt', 'Aunt'),
    ('grandmother', 'Grandmother'),
    ('grandfather', 'Grandfather'),
    ('other', 'Other'),
]

EDUCATION_LEVEL_CHOICES = [
    ('none', 'No Formal Education'),
    ('primary', 'Primary'),
    ('secondary', 'Secondary'),
    ('highschool', 'High School'),
    ('diploma', 'Diploma'),
    ('bachelor', "Bachelor's Degree"),
    ('master', "Master's Degree"),
    ('phd', 'PhD'),
    ('other', 'Other'),
]

class Parent(models.Model):
    """
    Student's Parent Module
    """
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=RELATION_CHOICES)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    education_level = models.CharField(max_length=100, choices=EDUCATION_LEVEL_CHOICES, null=True, blank=True)
    ocupation = models.CharField(max_length=100, null=True, blank=True)
    work_place = models.CharField(max_length=50, null=True, blank=True)
    # father_phone_no = models.IntegerField()
    image_file = models.ImageField(null=True, blank=True, upload_to="pic", default="knowledge1_aFn8hfk.jpg")
    registration_date = models.DateField(auto_now_add=True)
    city = models.CharField(max_length=50, default="Sheger")
    kfle_ketema = models.CharField(max_length=50, default="Gelanguda")
    wereda= models.CharField(max_length=50, default="Daletiy")
    hous_number = models.CharField(max_length=50, default="New")
    nationality = models.CharField(max_length=70, choices=COUNTRY_CHOICES, default="Ethiopia")
    email = models.EmailField(max_length=254, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    # registerd_date = models.DateTimeField(auto_now_add=True)
    registerd_date = models.DateTimeField(default=timezone.now)
    signature = models.ImageField(
        upload_to="signatures/",  # folder inside MEDIA_ROOT
        blank=True,
        null=True)
    
    class Meta:
        # ordering = ["-registerd_date"]
        ordering = ["-registerd_date"]

    def __str__(self):
        return f"{self.id} {self.first_name} {self.middle_name} {self.last_name} ({self.role})"
        

class PhoneNumber(models.Model):
    """Phone number model
    """
    parent = models.ForeignKey('Parent', on_delete=models.CASCADE, related_name='phone_numbers')
    # student = models.ForeignKey(StudentRegistration, on_delete=models.SET_NULL, null=True)   #? required or not?
    number = models.CharField(max_length=60)
    owner = models.CharField(max_length=30, choices=[('father', 'Father'), ('mother', 'Mother'), ('uncle', 'Uncle'), ('other', 'Other') ], null=True, blank=True)
    phone_type = models.CharField(max_length=30, choices=[('personal', 'Personal'), ('work phone', 'Work Phone'), ('other', 'Other')], null=True, blank=True)
    registerd_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-registerd_date"]

    def __str__(self):
        """ To print out the values.
        """
        return f" {self.parent}: {self.number}"

class EmergencyContact(models.Model):
    """Emergency contact for a student.
    """
    student = models.ForeignKey(StudentRegistration, on_delete=models.CASCADE, related_name="emergency", null=True, blank=True)
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True,)
    phone_num = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE, null=True, blank=True)  # phone_num &phone_number b/c to relate or to register a new respectively.


    # For non-parents (Uncle, Neighbor, etc.)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    relationship = models.CharField(max_length=100, choices=RELATION_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    registration_date = models.DateField(auto_now_add=True)
    image_file = models.ImageField(null=True, blank=True, upload_to="images/", default="jp.png")
    city = models.CharField(max_length=50, default="Sheger")
    kfle_ketema = models.CharField(max_length=50, default="Gelanguda")
    wereda= models.CharField(max_length=50, default="Daletiy")
    hous_number = models.CharField(max_length=50, default="New")
    nationality = models.CharField(max_length=70, choices=COUNTRY_CHOICES, default="Ethiopia")
    signature = models.ImageField(
        upload_to="signatures/",  # folder inside MEDIA_ROOT
        blank=True,
        null=True)
    email = models.EmailField(max_length=254, blank=True, null=True, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True, unique=True)

    class Meta:
        ordering = ["-registration_date"]


    def __str__(self):
        """ To print out the values.
        """
        return f"{self.student} {self.parent}: {self.phone_num}"
