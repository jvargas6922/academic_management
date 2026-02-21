from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Enrollment
from apps.students.models import Student
from apps.courses.models import Course
from .forms import EnrollmentForm
# Create your views here.
def index(request):
    enrollments = Enrollment.objects.all()
    return render(request, 'enrollment/enrollment_list.html', {'enrollments': enrollments})

def create_enrollment(request):
    """
    SIN APLICACION DE FORMULARIOS DE DJANGO
    """    
    # students = Student.objects.all()
    # courses = Course.objects.all()
    # context = {
    #     'students': students,
    #     'courses': courses
    # }
    # if requests.method == 'POST':
    #     try:
    #         # capturamos los datos del formulario (id del estudiante y del curso)
    #         student_id = requests.POST["student"]
    #         course_id = requests.POST["course"]
    #         # obtenemos las instancias de Student y Course a partir de los ids
    #         student = Student.objects.get(id=student_id)
    #         course = Course.objects.get(id=course_id)
    #         enrollment = Enrollment(student=student, course=course)
    #         # guardamos la nueva inscripción en la base de datos
    #         enrollment.save()
    #         messages.success(requests, 'Inscripción creada exitosamente')
    #         return render(requests, 'enrollment/create.html', context)
    #     except Exception as e:
    #         messages.error(requests, f'Error al crear la inscripción: {str(e)}')
    #         return render(requests, 'enrollment/create.html', context)
    
    # # Forma 1
    # return render(requests, 'enrollment/create.html', context)
    # # forma 2
    # # return render(requests, 'enrollment/create.html', {'students': students, 'courses': courses})
    """
    CON LA APLICACION DE FORMULARIOS DE DJANGO
    """
    if request.method == 'POST':
        try:
            form = EnrollmentForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Inscripción creada exitosamente')
                return redirect('enrollment_list')
        except Exception as e:
            messages.error(request, f'Error al crear la inscripción: {str(e)}')
    else:
        students = Student.objects.all()
        courses = Course.objects.all()
        context = {
            'students': students,
            'courses': courses,
            'form': EnrollmentForm()
        }
    return render(request, 'enrollment/create.html', context)

def edit(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    form = EnrollmentForm(instance=enrollment)
    context = {
        'form': form,
        'enrollment': enrollment
    }
    return render(request, 'enrollment/edit.html', context)

def update(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == "POST":
        try:
            form = EnrollmentForm(request.POST, instance=enrollment)
            if form.is_valid():
                form.save()
                messages.success(request, "Inscripción actualizada exitosamente")
                return redirect('enrollment_list')
        except Exception as e:
            messages.error(request, f"Error al actualizar la inscripción: {str(e)}") 
    else:
        form = EnrollmentForm(instance=enrollment)
        context = {
            'form': form,
            'enrollment': enrollment
        }
    return render(request, 'enrollment/edit.html', context)

def delete(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    try:
        enrollment.delete()
        messages.success(request, "Inscripción eliminada exitosamente")
    except Exception as e:
        messages.error(request, f"Error al eliminar la inscripción: {str(e)}")
    return redirect('enrollment_list')