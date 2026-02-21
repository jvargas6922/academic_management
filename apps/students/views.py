from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Student
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    students = Student.objects.all()
    # return HttpResponse("Hola desde el modulo estudiantes")

    return render(request, 'student/student_list.html', {'students': students})

    # otra forma de escribir y poder renderizar la plantilla
    # return render(request=request, template_name="students/index.html")

def create(request):
    if request.method == "POST":
        try:
            first_name = request.POST["first_name"] # otra forma de escribirlo
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            birth_date = request.POST["birth_date"]
            student = Student(
                first_name=first_name, 
                last_name=last_name, 
                email=email, 
                birth_date=birth_date
                )
            student.save()
            messages.success(request, "Estudiante creado exitosamente")
            # return redirect('list_students')
            return render(request, 'student/create.html')
        except Exception as e:
            messages.error(request, f"Error al crear el estudiante: {str(e)}")
        
    return render(request, 'student/create.html')

def edit(request, student_id):
    # este metodo me retorna el objeto o un error 404 si no lo encuentra
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'student/edit.html', {'student': student})

def update(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        try:
            # captura de los datos del formulario
            first_name = request.POST["first_name"] # otra forma de escribirlo
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            birth_date = request.POST["birth_date"]
            # actualización de los campos del estudiante
            student.first_name = first_name
            student.last_name = last_name
            student.email = email
            student.birth_date = birth_date
            student.save()
            messages.success(request, "Estudiante actualizado exitosamente")
            return redirect('list_students')
        except Exception as e:
            messages.error(request, f"Error al actualizar el estudiante: {str(e)}")
    return render(request, 'student/edit.html', {'student': student})

def delete(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    try:
        student.delete()
        messages.success(request, "Estudiante eliminado exitosamente")
        return redirect('list_students')
    except Exception as e:
        messages.error(request, f"Error al eliminar el estudiante: {str(e)}")
    return redirect('list_students')
