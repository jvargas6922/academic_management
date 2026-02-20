from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "description", "start_date"]
        labels = {
            "name": "Nombre",
            "description": "Descripción",
            "start_date": "Fecha de inicio",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control","placeholder": "Ingrese el nombre del curso","required": True}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Ingrese la descripción del curso", "rows": 4, "required": True}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date", "required": True}, format="%Y-%m-%d"),
        }