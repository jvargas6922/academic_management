from django.shortcuts import render, redirect
from .models import Course
from django.contrib import messages
# Create your views here.

def index(requests):
    courses = Course.objects.all()
    return render(requests, 'course/course_list.html', {'courses': courses})

def create_course(requests):
    if requests.method == 'POST':
        try:
            name = requests.POST["name"]
            description = requests.POST["description"]
            start_date = requests.POST["start_date"]
            course = Course(
                name = name,
                description = description,
                start_date = start_date
            )
            course.save()
            messages.success(requests, "Curso creado exitosamente")
            return render(requests, 'course/create.html')
        except Exception as e:
            messages.error(requests, f"Error al crear el curso: {str(e)}")
    return render(requests, 'course/create.html')