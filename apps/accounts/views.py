from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm, RegisterUserForm
from django.contrib import messages

# Create your views here.
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")  # Redirige a la página principal después de iniciar sesión
    else:
        form = LoginForm(request)
    return render(request, "account/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")  # Redirige a la página de inicio de sesión después de cerrar sesión

def register_view(request):
    if request.method == "POST":
        try:
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("login")  # Redirige a la página de inicio de sesión después de registrarse
        except Exception as e:
            # form.add_error(None, f"Error al registrar el usuario: {str(e)}")  # Agrega un error no relacionado con un campo específico
            messages.error(request, f"Error al registrar el usuario: {str(e)}")
            print(f"Error al registrar el usuario: {str(e)}")  # Imprime el error en la consola para depuración
    else:
        form = RegisterUserForm()
    return render(request, "account/register.html", {"form": form})