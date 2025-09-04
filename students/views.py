from django.shortcuts import render, redirect

from .forms import StudentRegistrationForm, EnrollmentFormSet, AcademicYearForm
from .models import AcademicYear, Enrollment
from parents.models import Parent

# Create your views here.

STEPS = [ "parent", "phone", "student", "emergency", "payment"]

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
    total_step = len(STEPS)
    current_step = STEPS.index("student") + 1

    student_form = StudentRegistrationForm()
    enrollment_formset = EnrollmentFormSet(request.POST, prefix='enroll')
    if request.method == "POST":
        student_form = StudentRegistrationForm(request.POST, request.FILES)
        enrollment_formset = EnrollmentFormSet(request.POST, prefix='enroll')

        request.session["current_step"] = request.session.get("current_step", 1) + 1
        request.session.modified = True

        if student_form.is_valid():
            student = student_form.save()
            # enrollment_formset.instance = students
            request.session["student_id"] = student.id  # store for next steps

            parent_ids = request.session.get("parent_ids", [])
            student.parents.set(Parent.objects.filter(id__in=parent_ids))
            student.save()
            
            enrollment_formset = EnrollmentFormSet(
                request.POST,
                instance=student,
                prefix="enroll",
            )

            if enrollment_formset.is_valid():
                enrollment_formset.save()
                # return redirect("pay", student_id=student.id)
                return redirect("emrgncy_info")
        else:
            # re-render with errors
            return render(request, "students/registration.html", {
                "form": student_form,
                "enrollment_formset": enrollment_formset,
            })
    else:
        student_form = StudentRegistrationForm()
        request.session["current_step"] = 3
        request.session.modified = False

        enrollment_formset = EnrollmentFormSet(prefix='enroll')
        

    return render(request, "students/registration.html", {
        "form": student_form,
        "enrollment_formset": enrollment_formset,
        "current_step": current_step,
        "total_step": total_step,
        })

def academicYear_register(request):
    """ Academic Year registration.
    """
    # form = AcademicYearForm()

    if request.method == "POST":
        form = AcademicYearForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("succes")
    else:
        form = AcademicYearForm()

    return render(request, "students/academy.html", {
        "form": form
    })

def success(request):
    """Display success message after registration.
    """
    return render(request, "students/success.html")
