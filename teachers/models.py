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
    # phone_no = models.IntegerField() ?


class PhoneNumber(models.Model):
    """Phone number model
    """
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='phone_numbers')
    number = models.CharField(max_length=60)

    # grade and section, what cours/subject, result of subject,
    # dose he/she teach, student got from grade and section, parent and admin may be, cv and id/pasport later
