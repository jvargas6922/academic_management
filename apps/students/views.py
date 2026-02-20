from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
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
        try:
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
            messages.success(requests, "Estudiante creado exitosamente")
            # return redirect('list_students')
            return render(requests, 'student/create.html')
        except Exception as e:
            messages.error(requests, f"Error al crear el estudiante: {str(e)}")
        
    return render(requests, 'student/create.html')

def edit(requests, student_id):
    # este metodo me retorna el objeto o un error 404 si no lo encuentra
    student = get_object_or_404(Student, id=student_id)
    return render(requests, 'student/edit.html', {'student': student})

def update(requests, student_id):
    student = get_object_or_404(Student, id=student_id)
    if requests.method == "POST":
        try:
            # captura de los datos del formulario
            first_name = requests.POST["first_name"] # otra forma de escribirlo
            last_name = requests.POST["last_name"]
            email = requests.POST["email"]
            birth_date = requests.POST["birth_date"]
            # actualización de los campos del estudiante
            student.first_name = first_name
            student.last_name = last_name
            student.email = email
            student.birth_date = birth_date
            student.save()
            messages.success(requests, "Estudiante actualizado exitosamente")
            return redirect('list_students')
        except Exception as e:
            messages.error(requests, f"Error al actualizar el estudiante: {str(e)}")
    return render(requests, 'student/edit.html', {'student': student})

def delete(requests, student_id):
    student = get_object_or_404(Student, id=student_id)
    try:
        student.delete()
        messages.success(requests, "Estudiante eliminado exitosamente")
        return redirect('list_students')
    except Exception as e:
        messages.error(requests, f"Error al eliminar el estudiante: {str(e)}")
