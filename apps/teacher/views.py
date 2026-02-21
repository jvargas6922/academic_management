from django.shortcuts import render, redirect, get_object_or_404
from .models import Teacher
from apps.courses.models import Course
from .forms import TeacherForm
# Create your views here.
def index(request):
    teachers = Teacher.objects.all()
    return render(request, "teacher/teacher_list.html", {"teachers": teachers})

def create(request):
    courses = Course.objects.all()
    if request.method == "POST":
        try:
            form = TeacherForm(request.POST)
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
    return render(request, "teacher/create.html", context)

def edit(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    courses = Course.objects.all()
    form = TeacherForm(instance=teacher)
    context ={
        "form": form,
        "teacher": teacher,
        "courses": courses
    }
    return render(request, "teacher/edit.html", context)

def update(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == "POST":
        try:
            form = TeacherForm(request.POST, instance=teacher)
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
    return render(request, "teacher/edit.html", context)

def delete(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    try:
        teacher.delete()
    except Exception as e:
        print(f"Error al eliminar el profesor: {e}")
    return redirect("teacher_list")
