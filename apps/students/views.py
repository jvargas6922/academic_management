from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Student

# Create your views here.
def index(requests):
    students = Student.objects.all()
    # return HttpResponse("Hola desde el modulo estudiantes")

    return render(requests, 'student/student_list.html', {'students': students})

    # otra forma de escribir y poder renderizar la plantilla
    # return render(request=requests, template_name="students/index.html")

def create(requests):
    if requests.method == "POST":
        first_name = requests.POST["first_name"] # otra forma de escribirlo
        last_name = requests.POST["last_name"]
        email = requests.POST["email"]
        birth_date = requests.POST["birth_date"]
        student = Student(
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            birth_date=birth_date
            )
        student.save()
        return redirect('students:index')
    return render(requests, 'student/create.html')
        
