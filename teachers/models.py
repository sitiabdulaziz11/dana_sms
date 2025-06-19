from django.db import models

# Create your models here.

class Teacher(models.Model):
    """
    Teacher model that represents teacher's fields/attributes.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=15)
    age = models.IntegerField()
    image_file = models.ImageField()
    address = models.CharField(max_length=60)
    hiring_date = models.DateField(auto_now_add=True)
    phone_no = models.IntegerField()
