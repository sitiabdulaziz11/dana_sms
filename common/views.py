from django.shortcuts import render, redirect

from .forms import GradeForm, SectionForm
from .models import Grade, Section

# Create your views here.

def gradeSection_register(request):
    """Models that registaer grade.
    """
    if request.method == "POST":
        grade_form = GradeForm(request.POST)
        section_form = SectionForm(request.POST)

        grades = Grade.objects.all()
        sections = Section.objects.all()

        if grade_form.is_valid():
            g_name = grade_form.cleaned_data.get("grade_name")
            print(g_name)

            if grades.filter(grade_name=g_name).exists():
                pass
            else:
                grade_form.save()

        if section_form.is_valid():
            s_name = section_form.cleaned_data.get("section_name")
            print(s_name)
            
            if sections.filter(section_name=s_name).exists():
                pass
            else:
                section_form.save()
            return redirect("/admin/common/")
        else:
            print("Is section form valid?", section_form.is_valid())
            print(section_form.errors)
            return redirect("grade_reg")
        
    else:
        grade_form = GradeForm()
        section_form = SectionForm()
    return render(request, "common/grade_section_reg.html", {
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
