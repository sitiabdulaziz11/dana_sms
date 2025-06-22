from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from students.models import Student

# Create your models here.


class Grade(models.Model):
    """Grade model that specify students grade level.
    """
    grade_name = models.CharField(max_length=30)

class Section(models.Model):
    """Models which define students section.
    """

class Subject(models.Model):
    """Subject model that represents subject's fields/attributes.
    """
    subject_name = models.CharField(max_len=120)
    # teacher ,students, sub_results, results

# class Term(models.Model)
class Semester(models.Model):
    """Models that specify the semester of the year.
    """
    semester_name = models.CharField(max_length=60)


class Result(models.Model):
    """Result model that represents result's fields/attributes.
    """
    Total_score = 
Total_average
Rank
date
subject_id
student_id
teacher_id
subject_result


class SubjectResult():
    """SubjectResult model that represents one subject result.
    """
    test1_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    test2_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    test3_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True)
    assisgnment = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True)
    worksheer = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    mid_exam = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    exer_book = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    final_exam = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator()])
    
    totalScore = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    sub_rank = models.IntegerField()

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
