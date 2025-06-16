from django.db import models

# Create your models here.

class Student(models.Model):
    """Studentes information.
    """
    first_name = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    password = 
    birth_date = models.DateField(null=True, blank=True)
    age = models.IntegerField()
    image_file = models.ImageField()
    address = models.CharField(max_length=60)
    registration_date = models.DateField(auto_now_add=True)

    # registration date =, phone_no from parent or? grade, section other separet table or?, email , password good or?

