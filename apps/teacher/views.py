from django.shortcuts import render, redirect,get_object_or_404
from .models import Teacher
from apps.courses.models import Course
from .forms import TeacherForm
# Create your views here.
def index(requests):
    teachers = Teacher.objects.all()
    return render(requests, "teacher/teacher_list.html", {"teachers": teachers})

def create(requests):
    courses = Course.objects.all()
    if requests.method == "POST":
        try:
            form = TeacherForm(requests.POST)
            if form.is_valid():
                form.save()
                return redirect("teacher_list")
        except Exception as e:
            print(f"Error al crear el profesor: {e}")
    else:
        form = TeacherForm()
        context ={
            "form": form,
            "courses": courses
        }
    return render(requests, "teacher/create.html", context)

def edit(requests, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    courses = Course.objects.all()
    form = TeacherForm(instance=teacher)
    context ={
        "form": form,
        "teacher": teacher,
        "courses": courses
    }
    return render(requests, "teacher/edit.html", context)

def update(requests, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if requests.method == "POST":
        try:
            form = TeacherForm(requests.POST, instance=teacher)
            if form.is_valid():
                form.save()
                return redirect("teacher_list")
        except Exception as e:
            print(f"Error al actualizar el profesor: {e}")
    else:
        form = TeacherForm(instance=teacher)
        context ={
            "form": form,
            "teacher": teacher
        }
    return render(requests, "teacher/edit.html", context)

def delete(requests, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    try:
        teacher.delete()
    except Exception as e:
        print(f"Error al eliminar el profesor: {e}")
    return redirect("teacher_list")
