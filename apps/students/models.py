from django.db import models

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"