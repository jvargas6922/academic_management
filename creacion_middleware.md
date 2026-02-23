# Creación de Middleware de Autenticación (paso a paso)

Este documento te explica cómo crear un middleware en tu proyecto Django para proteger todas tus vistas sin tener que agregar `@login_required` en cada método.

---

## 1) Objetivo

Queremos que:

- Si el usuario **no está autenticado**, no pueda entrar a rutas privadas.
- Se redirija automáticamente a `login`.
- Rutas públicas como `login`, `register`, `admin` y archivos estáticos queden permitidas.

---

## 2) Crear archivo del middleware

En tu proyecto, crea el archivo:

- `academic_management/academic_management/middleware.py`

Contenido sugerido:

```python
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse('login')

        public_paths = [
            login_url,
            reverse('register'),
            '/admin/',
            '/static/',
            '/media/',
        ]

        is_public_path = any(request.path.startswith(path) for path in public_paths)

        if not request.user.is_authenticated and not is_public_path:
            return redirect(f"{login_url}?next={request.path}")

        return self.get_response(request)
```

---

## 3) Registrar el middleware en `settings.py`

Archivo:

- `academic_management/academic_management/settings.py`

En `MIDDLEWARE`, agrégalo **después** de `AuthenticationMiddleware`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'academic_management.middleware.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

> Importante: debe ir después de `AuthenticationMiddleware` para que `request.user` exista correctamente.

---

## 4) Verificar que existan rutas públicas

Asegúrate de tener rutas con nombre:

- `login`
- `register`

Si usas logout:

- `logout`

Ejemplo en tu app de cuentas (`apps/accounts/urls.py`):

```python
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
```

Y en `academic_management/academic_management/urls.py` incluir:

```python
path('', include('apps.accounts.urls')),
```

---

## 5) Configurar redirecciones de autenticación

En `settings.py` agrega (si no existen):

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
```

---

## 6) Probar funcionamiento

Desde la carpeta donde está `manage.py`:

```bash
python manage.py runserver
```

Pruebas recomendadas:

1. Ir a `/students/` sin login -> debe redirigir a `/login/?next=/students/`.
2. Iniciar sesión -> debe permitir el acceso.
3. Ir a `/courses/`, `/enrollments/`, `/teachers/` sin login -> deben redirigir a login.
4. Verificar que `/login/` y `/register/` siguen accesibles sin sesión.

---

## 7) ¿Qué ventajas tiene este enfoque?

- No repites `@login_required` en cada función.
- Seguridad centralizada en un solo lugar.
- Menos riesgo de olvidar proteger una vista nueva.

---

## 8) Buenas prácticas

- Mantén una lista clara de rutas públicas en el middleware.
- Si agregas APIs públicas o páginas de ayuda, inclúyelas en exclusiones.
- Si usas archivos media en desarrollo, deja `/media/` como ruta pública.

---

## 9) Posibles errores comunes

1. **Error `NoReverseMatch` en `login` o `register`**
   - Falta la ruta con ese `name` en tus urls.

2. **Loop infinito de redirección a login**
   - No excluiste correctamente la ruta `login` en `public_paths`.

3. **`request.user` no disponible**
   - El middleware está antes de `AuthenticationMiddleware`.

---

## 10) Resumen

Con este middleware, tu proyecto queda protegido de forma global:

- No autenticado -> redirección a login.
- Autenticado -> acceso normal.
- Rutas públicas -> disponibles sin sesión.

Es la forma más práctica para tu proyecto cuando tienes muchas vistas basadas en funciones.

---

## 11) Explicación de cada instrucción (qué hace y por qué)

### 11.1 Bloque del middleware línea por línea

Código de referencia:

```python
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
        def __init__(self, get_response):
                self.get_response = get_response

        def __call__(self, request):
                login_url = reverse('login')

                public_paths = [
                        login_url,
                        reverse('register'),
                        '/admin/',
                        '/static/',
                        '/media/',
                ]

                is_public_path = any(request.path.startswith(path) for path in public_paths)

                if not request.user.is_authenticated and not is_public_path:
                        return redirect(f"{login_url}?next={request.path}")

                return self.get_response(request)
```

Explicación:

- `from django.shortcuts import redirect`
    - Importa la función para responder con una redirección HTTP.

- `from django.urls import reverse`
    - Permite construir URL por nombre de ruta (`login`, `register`) sin escribir la ruta “a mano”.

- `class LoginRequiredMiddleware:`
    - Define una clase middleware que intercepta **todas** las peticiones.

- `def __init__(self, get_response):`
    - Django entrega la función `get_response` para continuar el flujo normal de la petición.

- `self.get_response = get_response`
    - Guarda esa función para usarla al final cuando la petición sí deba continuar.

- `def __call__(self, request):`
    - Método que se ejecuta en cada request entrante.

- `login_url = reverse('login')`
    - Obtiene dinámicamente la URL de login (por ejemplo `/login/`).

- `public_paths = [...]`
    - Lista de rutas que no requieren autenticación:
        - `login_url`: para que puedas entrar a login.
        - `reverse('register')`: para permitir registro.
        - `'/admin/'`: para no bloquear acceso al admin.
        - `'/static/'` y `'/media/'`: para cargar archivos estáticos/media.

- `is_public_path = any(request.path.startswith(path) for path in public_paths)`
    - Revisa si la ruta actual comienza con alguna ruta pública.

- `if not request.user.is_authenticated and not is_public_path:`
    - Condición central: si no hay sesión iniciada y la ruta no es pública, se bloquea.

- `return redirect(f"{login_url}?next={request.path}")`
    - Redirige a login y agrega `next` para volver a la página original tras autenticar.

- `return self.get_response(request)`
    - Si cumple reglas (autenticado o ruta pública), deja continuar el request.

### 11.2 Qué hace cada instrucción del paso 3 (`MIDDLEWARE` en settings)

- `'django.contrib.auth.middleware.AuthenticationMiddleware'`
    - Carga `request.user` para saber si el usuario está autenticado.

- `'academic_management.middleware.LoginRequiredMiddleware'`
    - Activa tu middleware global de protección de rutas.

- Orden correcto
    - Tu middleware debe ir **después** de `AuthenticationMiddleware`, de lo contrario `request.user` no estará disponible.

### 11.3 Qué hace cada instrucción del paso 4 (rutas públicas)

- `path('login/', ..., name='login')`
    - Define una URL de login con nombre `login` para que `reverse('login')` funcione.

- `path('register/', ..., name='register')`
    - Define la ruta de registro con nombre `register`.

- `path('logout/', ..., name='logout')`
    - Permite cerrar sesión con nombre `logout`.

- `path('', include('apps.accounts.urls'))`
    - Incluye las rutas de `accounts` en el enrutador principal del proyecto.

### 11.4 Qué hace cada ajuste del paso 5 (settings de auth)

- `LOGIN_URL = 'login'`
    - URL por defecto de redirección cuando una ruta requiere autenticación.

- `LOGIN_REDIRECT_URL = 'home'`
    - Destino por defecto al iniciar sesión exitosamente.

- `LOGOUT_REDIRECT_URL = 'login'`
    - Destino al cerrar sesión.

### 11.5 Qué valida cada prueba del paso 6

- Entrar a `/students/` sin login
    - Verifica que el middleware está bloqueando rutas privadas.

- Iniciar sesión
    - Verifica que un usuario autenticado sí puede navegar rutas privadas.

- Entrar a `/courses/`, `/enrollments/`, `/teachers/` sin login
    - Verifica que la protección aplica de forma global, no solo en una app.

- Abrir `/login/` y `/register/` sin sesión
    - Verifica que las excepciones públicas están bien definidas.
