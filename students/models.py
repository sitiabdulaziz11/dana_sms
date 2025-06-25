from django.db import models
from django.contrib.auth.models import User

from parents.models import Parent

# Create your models here.

class StudentRegistration(models.Model):
    """Studentes information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    first_name = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=15)
    # email = models.EmailField(max_length=254, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    age = models.IntegerField()
    image_file = models.ImageField()
    address = models.CharField(max_length=60)
    registration_date = models.DateField(auto_now_add=True)
    kebele_wereda = models.CharField(max_length=50)
    kfleketema = models.CharField(max_length=50)
    hous_number = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)

    # Relations
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    # phone_no from parent or? grade, section other separet table or?, email , password good or?
    # result, teachers, subjects, admin and parent.

    # def __str__(self):
    #     return f"{self.first_name} {self.last_name}"
