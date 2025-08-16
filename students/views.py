from django.shortcuts import render

# Create your views here.

def main_page(request):
    """To display main or home page
    """
    return render(request, "students/index.html")

def dashboards(request):
    """To display main or home page
    """
    return render(request, "students/dashboards.html")


# def register_student(request):
#     """To register students
#     """
#     if request.method == "POST":
#         student = 
