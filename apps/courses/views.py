from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from django.contrib import messages
from .forms import CourseForm
# Create your views here.

def index(request):
    courses = Course.objects.all()
    return render(request, 'course/course_list.html', {'courses': courses})

def create_course(request):
    """
    SIN IMPLEMENTACION DE FORMULARIO
    """
    # if requests.method == 'POST':
    #     try:
    #         name = requests.POST["name"]
    #         description = requests.POST["description"]
    #         start_date = requests.POST["start_date"]
    #         course = Course(
    #             name = name,
    #             description = description,
    #             start_date = start_date
    #         )
    #         course.save()
    #         messages.success(requests, "Curso creado exitosamente")
    #         return render(requests, 'course/create.html')
    #     except Exception as e:
    #         messages.error(requests, f"Error al crear el curso: {str(e)}")
    # return render(requests, 'course/create.html')
    """
    CON IMPLEMENTACION DE FORMULARIO
    """
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Curso creado exitosamente")
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'course/create.html', {'form': form})

def edit(request, course_id):
    course = get_object_or_404(Course, id= course_id)
    form = CourseForm(instance=course)
    context = {
        'form': form,
        'course': course
    }
    return render(request, 'course/edit.html', context)

def update(request, course_id):
    course = get_object_or_404(Course, id= course_id)
    if request.method == 'POST':
        try:
            form = CourseForm(request.POST, instance=course)
            if form.is_valid():
                form.save()
                messages.success(request, "Curso actualizado exitosamente")
                return redirect('course_list')
        except Exception as e:
            messages.error(request, f"Error al actualizar el curso: {str(e)}")
    else:
        form = CourseForm(instance=course)
        context = {
            'form': form,
            'course': course
        }
    return render(request, 'course/edit.html', context)

def delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    try:
        course.delete()
        messages.success(request, "Curso eliminado exitosamente")
    except Exception as e:
        messages.error(request, f"Error al eliminar el curso: {str(e)}")
    return redirect('course_list')