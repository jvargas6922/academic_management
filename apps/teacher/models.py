from django.db import models

# Create your models here.
class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='teacher')

    def __str__(self):
        return f"{self.first_name} {self.last_name} y enseña el curso {self.course.name}"
