from django.shortcuts import render, redirect

from .forms import StudentRegistrationForm
from .models import AcademicYear, Enrollment

# Create your views here.

def main_page(request):
    """To display main or home page
    """
    return render(request, "students/index.html")

def dashboards(request):
    """To display main or home page
    """
    return render(request, "students/dashboards.html")


def register_student(request):
    """To register students
    """
    form = StudentRegistrationForm()
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            students = form.save()

            # Get the current active academic year
            current_year = AcademicYear.objects.filter(is_active=True).first()

            # Create enrollment record
            Enrollment.objects.create(
                student=students,
                grade=students.grade,
                section=students.section,
                academic_year=current_year
            )
            # return redirect("succ")
            return redirect("pay", student_id=students.id)
        else:
            form = StudentRegistrationForm()
    return render(request, "students/registration.html", {"form": form})

def success(request):
    """Display success message after registration.
    """
    return render(request, "students/success.html")
