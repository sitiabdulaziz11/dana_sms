from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    """Studentes information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

    # phone_no from parent or? grade, section other separet table or?, email , password good or?

    # def __str__(self):
    #     return f"{self.first_name} {self.last_name}"
