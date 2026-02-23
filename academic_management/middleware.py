from django.shortcuts import redirect
from django.urls import reverse

class LoginRequieredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse('login')

        public_paths = [
            login_url,
            reverse('register'),
            '/students/',  # Permitir acceso a la lista de estudiantes sin autenticación
            '/admin/',  # Permitir acceso al panel de administración
            '/static/',
            '/media/',
            ] 
        
        is_public_path = any(request.path.startswith(path) for path in public_paths)
        if not request.user.is_authenticated and not is_public_path:
            return redirect(f"{login_url}?next={request.path}")

        return self.get_response(request)

    