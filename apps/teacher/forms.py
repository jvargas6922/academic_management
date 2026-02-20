from django import forms
from .models import Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "course"]
        labels ={
            "first_name": "Nombre",
            "last_name": "Apellido",
            "course": "Curso"
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control","placeholder": "Ingrese el nombre del profesor","required": True}),
            "last_name": forms.TextInput(attrs={"class": "form-control","placeholder": "Ingrese el apellido del profesor","required": True}),
            "course": forms.Select(attrs={"class": "form-select","required": True}),
        }