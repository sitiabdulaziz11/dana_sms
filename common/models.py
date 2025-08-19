from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from students.models import StudentRegistration

# Create your models here.


class Grade(models.Model):
    """Grade model that specify students grade level.
    """
    grade_name = models.CharField(max_length=30)

    def __str__(self):
        return f" Grade {self.grade_name}"

class Section(models.Model):
    """Models which define students section.
    """
    section_name = models.CharField(max_length=30)

# class Term(models.Model)
class Semester(models.Model):
    """Models that specify the semester of the year.
    """
    semester_name = models.CharField(max_length=60)
    year = models.IntegerField()

class Subject(models.Model):
    """Subject model that represents subject's fields/attributes.
    """
    subject_name = models.CharField(max_length=120)
    # teacher ,students, sub_results, results

class Result(models.Model):
    """Result model that represents result's fields/attributes.
    """
    student = models.ForeignKey(StudentRegistration, on_delete=models.CASCADE)
    Total_score = models.FloatField(null=True, blank=True)
    Total_average = models.FloatField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

class SubjectResult(models.Model):
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
    final_exam = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(30)])
    
    totalScore = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    sub_rank = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    student = models.ForeignKey(StudentRegistration, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def calculate_total_score(self):
        components = [
            self.test1_score, self.test2_score, self.test3_score,
            self.assignment, self.worksheet, self.mid_exam,
            self.exer_book, self.final_exam
        ]
        self.total_score = sum(filter(None, components)) if any(components) else 0
        self.save()
