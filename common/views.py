from django.shortcuts import render, redirect

from .forms import GradeForm, SectionForm

# Create your views here.

def gradeSection_register(request):
    """Models that registaer grade.
    """
    if request.method == "POST":
        grade_form = GradeForm(request.POST)
        section_form = SectionForm(request.POST)
        if grade_form.is_valid() and section_form.is_valid():
            grade_form.save()
            section_form.save()
            return redirect("succes")
    else:
        grade_form = GradeForm()
        section_form = SectionForm()
    return render(request, "common/registration.html", {
        "g_form": grade_form,
        "s_form": section_form,
        })


def admins_page (request):
    """Admin dashboard page.
    """
    
    return render(request, "common/admins_page.html")


# def section_register(request):
#     """Register section.
#     """
#     if request.method == "POST":
#         form = SectionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("succes")
#     else:
#         form = SectionForm()
#     return render(request, "common/registration.html", {"form" : form})

def success(request):
    """To handle success message.
    """
    return render(request, "common/success.html")
