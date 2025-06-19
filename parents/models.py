from django.db import models

# Create your models here.

class Parent(models.Model):
    """
    Student's Parent Module
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    father_first_name = models.CharField(max_length=100)
    father_middlename = models.CharField(max_length=100)
    father_last_name = models.CharField(max_length=100)
    father_age = models.IntegerField()
    # father_phone_no = models.IntegerField()
    father_image_file = models.ImageField()
    mother_first_name = models.CharField(max_length=100)
    mother_middlename = models.CharField(max_length=100)
    mother_last_name = models.CharField(max_length=100)
    mother_age = models.IntegerField()
    # mother_phone_no = models.IntegerField()
    mother_image_file = models.ImageField()
    address = models.CharField(max_length=60)


class PhoneNumber(models.Model):
    """Phone number model
    """
    parent = models.ForeignKey('Parent', on_delete=models.CASCADE, related_name='phone_numbers')
    number = models.CharField(max_length=60)
    owner = models.CharField(max_length=30, choices=[('father', 'Father'), ('mother', 'Mother')])
