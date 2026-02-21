# Implementación de Login, Register y Logout (ajustada a tu código actual)

Este documento está hecho sobre el estado real de tu proyecto `academic_management`.

## 0) Contexto real detectado en tu proyecto

- Usas Django 4.2.28.
- `home` hoy está en `apps/core/views.py` como función `home`.
- Tu `academic_management/urls.py` actualmente enruta:
  - `''` -> `views.home`
  - `students/`, `courses/`, `enrollments/`, `teachers/`
- Todas tus vistas CRUD son **funciones** (FBV), no clases.
- Tu navegación principal está en `templates/base.html`.

Por lo tanto, la forma más limpia para tu caso es:
1) mantener `apps.core` para autenticación,
2) crear `apps/core/urls.py`,
3) proteger vistas con `@login_required`.

---

## 1) Configuración en `settings.py`

Archivo: `academic_management/academic_management/settings.py`

Al final del archivo, agrega:

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
```

Con esto:
- si un usuario no autenticado entra a una vista protegida, Django lo envía a `/login/`.
- al hacer login, se redirige a `home`.
- al hacer logout, vuelve a login.

---

## 2) Crear formulario de registro

### 2.1 Crear archivo

Crea `apps/core/forms.py`:

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
```

---

## 3) Actualizar vistas de `core`

Archivo actual: `apps/core/views.py`

Hoy tienes:

```python
def home(requests):
    return render(requests, 'home.html')
```

Debes dejarlo así (manteniendo tu estilo de función):

```python
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


def register_view(requests):
    if requests.user.is_authenticated:
        return redirect('home')

    if requests.method == 'POST':
        form = RegisterForm(requests.POST)
        if form.is_valid():
            user = form.save()
            login(requests, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(requests, 'auth/register.html', {'form': form})


@login_required
def home(requests):
    return render(requests, 'home.html')
```

> Nota: mantengo el nombre `home` para que no rompa tu `urlpatterns` actual.

---

## 4) Crear rutas de autenticación en `core`

### 4.1 Crear `apps/core/urls.py`

```python
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
]
```

### 4.2 Actualizar rutas globales

Archivo: `academic_management/academic_management/urls.py`

Actualmente importas `from apps.core import views` y usas `path('', views.home, name='home')`.

Cámbialo para incluir `core.urls`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('students/', include('apps.students.urls')),
    path('courses/', include('apps.courses.urls')),
    path('enrollments/', include('apps.enrollments.urls')),
    path('teachers/', include('apps.teacher.urls')),
]
```

---

## 5) Crear templates de autenticación

### 5.1 Crear carpeta

- `templates/auth/`

### 5.2 `templates/auth/login.html`

```html
{% extends 'base.html' %}

{% block title %}Iniciar sesión{% endblock %}

{% block content %}
<div class="container mt-4" style="max-width: 500px;">
  <h2 class="text-center">Iniciar sesión</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary w-100">Entrar</button>
  </form>
  <p class="mt-3 text-center">¿No tienes cuenta? <a href="{% url 'register' %}">Regístrate</a></p>
</div>
{% endblock %}
```

### 5.3 `templates/auth/register.html`

```html
{% extends 'base.html' %}

{% block title %}Registro{% endblock %}

{% block content %}
<div class="container mt-4" style="max-width: 500px;">
  <h2 class="text-center">Crear cuenta</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-success w-100">Registrarse</button>
  </form>
  <p class="mt-3 text-center">¿Ya tienes cuenta? <a href="{% url 'login' %}">Inicia sesión</a></p>
</div>
{% endblock %}
```

---

## 6) Proteger tus rutas CRUD actuales (según nombres reales)

En tu proyecto todas las vistas son de función. Debes agregar `@login_required` en cada app.

## 6.1 Students (`apps/students/views.py`)

Proteger estas funciones:

- `index`
- `create`
- `edit`
- `update`
- `delete`

Ejemplo:

```python
from django.contrib.auth.decorators import login_required

@login_required
def index(requests):
    ...
```

## 6.2 Courses (`apps/courses/views.py`)

Proteger:

- `index`
- `create_course`
- `edit`
- `update`
- `delete`

## 6.3 Enrollments (`apps/enrollments/views.py`)

Proteger:

- `index`
- `create_enrollment`
- `edit`
- `update`
- `delete`

## 6.4 Teacher (`apps/teacher/views.py`)

Proteger:

- `index`
- `create`
- `edit`
- `update`
- `delete`

---

## 7) Ajustar menú en `base.html` con autenticación

Archivo: `templates/base.html`

Tu menú hoy siempre muestra los módulos (`student_list`, `course_list`, etc.).
Debes mostrar opciones según autenticación.

Ejemplo recomendado (adaptado a tus rutas):

```html
<nav>
    <ul class="nav justify-content-center">
        {% if user.is_authenticated %}
            <li class="nav-item"><a class="nav-link" href="{% url 'home' %}">Inicio</a></li>
            <li class="nav-item"><a class="nav-link" href="{% url 'student_list' %}">Estudiantes</a></li>
            <li class="nav-item"><a class="nav-link" href="{% url 'course_list' %}">Cursos</a></li>
            <li class="nav-item"><a class="nav-link" href="{% url 'enrollment_list' %}">Inscripciones</a></li>
            <li class="nav-item"><a class="nav-link" href="{% url 'teacher_list' %}">Profesores</a></li>
            <li class="nav-item"><a class="nav-link" href="{% url 'logout' %}">Cerrar sesión</a></li>
        {% else %}
            <li class="nav-item"><a class="nav-link" href="{% url 'login' %}">Iniciar sesión</a></li>
            <li class="nav-item"><a class="nav-link" href="{% url 'register' %}">Registrarse</a></li>
        {% endif %}
    </ul>
</nav>
```

---

## 8) Flujo esperado después de implementar

1. Usuario no autenticado entra a `/students/`.
2. Es redirigido a `/login/?next=/students/`.
3. Si inicia sesión correctamente:
   - vuelve a la ruta solicitada (`next`), o
   - va a `home` según el flujo.
4. Si hace logout, vuelve a `/login/`.

---

## 9) Comandos para probar

Desde la carpeta donde está `manage.py`:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Pruebas:

- `/register/` crea usuario.
- `/login/` autentica usuario.
- `/logout/` cierra sesión.
- `/students/`, `/courses/`, `/enrollments/`, `/teachers/` redirigen a login si no hay sesión.

---

## 10) Checklist final (específico de tu proyecto)

- [ ] `settings.py` con `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`.
- [ ] `apps/core/forms.py` creado con `RegisterForm`.
- [ ] `apps/core/views.py` con `register_view` y `home` protegido.
- [ ] `apps/core/urls.py` creado (`login`, `register`, `logout`, `home`).
- [ ] `academic_management/urls.py` usando `include('apps.core.urls')`.
- [ ] Templates creados: `templates/auth/login.html` y `templates/auth/register.html`.
- [ ] Decorador `@login_required` agregado en todas las vistas CRUD de:
  - `students`
  - `courses`
  - `enrollments`
  - `teacher`
- [ ] `templates/base.html` muestra menú según `user.is_authenticated`.

---

## 11) Nota técnica importante encontrada en tu código

En algunas vistas (`teacher.create`, `teacher.update`, `enrollments.create_enrollment`) el `context` se define solo en ramas específicas (`else`), lo que puede causar errores si hay POST inválido.

No impide implementar autenticación, pero si aparece `UnboundLocalError`, debes inicializar `context` antes del `if`.

---

Con este documento ya tienes una guía 100% alineada a tu estructura actual para implementar login/register/logout y proteger todo el CRUD.
