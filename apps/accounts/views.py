from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterUserForm
from django.contrib import messages

# Create your views here.
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")  # Redirige a la página principal después de iniciar sesión
            else:
                form.add_error(None, "Credenciales inválidas")
    else:
        form = LoginForm()
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
            messages.error(request, f"Error al registrar el usuario: {str(e)}")
            print(f"Error al registrar el usuario: {str(e)}")  # Imprime el error en la consola para depuración
    else:
        form = RegisterUserForm()
    return render(request, "account/register.html", {"form": form})