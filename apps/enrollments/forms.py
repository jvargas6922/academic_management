from django import forms
from .models import Enrollment

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["student", "course"]
        labels = {
            "student": "Estudiante",
            "course": "Curso",
        }
        widgets = {
            "student": forms.Select(attrs={"class": "form-select", "required": True}),
            "course": forms.Select(attrs={"class": "form-select", "required": True}),
        }