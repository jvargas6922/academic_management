from django.db import models

# Create your models here.
from  apps.students.models import Student
from  apps.courses.models import Course
class Enrollment(models.Model):
    
    # forma 1
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='enrollments') 
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        # establece que un estudiante no puede estar inscrito en el mismo curso más de una vez
        unique_together = ('student', 'course')  

    def __str__(self):
        return f"{self.student} inscrito en {self.course}"









    # forma 2
    #student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
