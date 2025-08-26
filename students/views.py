from django.shortcuts import render, redirect

from .forms import StudentRegistrationForm, EnrollmentFormSet
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
    student_form = StudentRegistrationForm()
    enrollment_formset = EnrollmentFormSet(request.POST, prefix='enroll')
    if request.method == "POST":
        student_form = StudentRegistrationForm(request.POST, request.FILES)
        enrollment_formset = EnrollmentFormSet(request.POST, prefix='enroll')

        # if student_form.is_valid() and enrollment_formset.is_valid():
        if student_form.is_valid():
            student = student_form.save()
            # enrollment_formset.instance = students

            enrollment_formset = EnrollmentFormSet(
                request.POST,
                instance=student,
                prefix="enroll",
            )
            # for enroll in enrollments:
            #     enroll.students = students
            #     enroll.save()

            # Get the current active academic year
            # current_year = AcademicYear.objects.filter(is_active=True).first()

            # # Create enrollment record
            # Enrollment.objects.create(
            #     student=students,
            #     grade=students.grade,
            #     section=students.section,
            #     academic_year=current_year
            # )
            # return redirect("succ")

            if enrollment_formset.is_valid():
                enrollment_formset.save()
                return redirect("pay", student_id=student.id)

            # return redirect("pay", student_id=students.id)
            # else:
            #     # Re-render with errors
            #     return render(request, "students/registration.html", {
            #         "form": student_form,
            #         "enrollment_formset": enrollment_formset,
            #     })
        # else:
        #     # student_form = StudentRegistrationForm()
        #     # enrollment_formset = EnrollmentFormSet(request.POST, prefix='enroll')
        #     return render(request, "students/registration.html", {
        #         "form": student_form,
        #         "enrollment_formset": enrollment_formset,
        #     })
    else:
        student_form = StudentRegistrationForm()
        enrollment_formset = EnrollmentFormSet(prefix='enroll')
    return render(request, "students/registration.html", {
        "form": student_form,
        "enrollment_formset": enrollment_formset
        })

def success(request):
    """Display success message after registration.
    """
    return render(request, "students/success.html")
