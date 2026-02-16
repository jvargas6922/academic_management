from django.shortcuts import render
from .models import Course
# Create your views here.

def index(requests):
    courses = Course.objects.all()
    return render(requests, 'course/course_list.html', {'courses': courses})

def create_course(requests):
    pass