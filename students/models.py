from django.db import models
from django.contrib.auth.models import User
import pycountry
from datetime import datetime


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
    birth_date = models.DateField(null=True, blank=True)
    age = models.IntegerField()

    grade = models.ForeignKey("common.Grade", on_delete=models.SET_NULL, null=True, related_name="students")
    section = models.ForeignKey("common.Section", on_delete=models.SET_NULL, null=True, related_name="students")
    
    image_file = models.ImageField()
    registration_date = models.DateField(auto_now_add=True)
    city = models.CharField(max_length=50)
    kfle_ketema = models.CharField(max_length=50)
    wereda= models.CharField(max_length=50)
    hous_number = models.CharField(max_length=50, null=True, blank=True)
    nationality = models.CharField(max_length=70, choices=COUNTRY_CHOICES)
    email = models.EmailField(max_length=254, blank=True, null=True, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True, unique=True)
    join_year = models.CharField(max_length=2, default=str(datetime.now().
    year)[-2:])
    # student_id = models.CharField(max_length=20, unique=True, blank=True)
    # prefix = models.CharField(max_length=10, default="A/D")  # editable

    # Relations
    # parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    # phone_no from parent or? grade, section other separet table or?, email , password good or?
    # result, teachers, subjects, admin and parent.

    # Relations
    
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
    
    # def save(self, *args, **kwargs):
    #     is_new = self.pk is None
    #     super().save(*args, **kwargs)

    #     if is_new and not self.student_id:
    #         self.student_id = f"{self.prefix}/{self.id}/{self.join_year}"
    #     super().save(update_fields=['student_id'])


    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

class AcademicYear(models.Model):
    """ To set academic year.
    """
    year = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """To save active year.
        """
        if self.is_active:
            AcademicYear.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.year


class Enrollment(models.Model):
    """Enrollment model to enrol students in each year.
    """
    student = models.ForeignKey(StudentRegistration, on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey("common.Grade", on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey("common.Section", on_delete=models.SET_NULL, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)

    class Meta:
        """ To make unique"""
        unique_together = ("student", "academic_year")

    def __str__(self):
        """ To print fildes """
        return f"{self.student} - {self.grade} {self.section} ({self.academic_year})"        
