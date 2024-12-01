from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.timezone import now

# Diccionario global para rastrear intentos de inicio de sesión y bloqueos
user_attempts = {}

def login_view(request):
    global user_attempts

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Comprobar si el usuario está bloqueado
        if username in user_attempts:
            attempts, lock_time = user_attempts[username]
            if attempts >= 3:
                if lock_time and (now() - lock_time).seconds < 15:
                    # Usuario bloqueado dentro de los 15 segundos
                    messages.error(request, 'Tu cuenta está bloqueada. Intenta de nuevo en 15 segundos.')
                    return render(request, 'login/login.html')
                else:
                    # Restablecer intentos después de 15 segundos
                    user_attempts[username] = (0, None)

        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            if username in user_attempts:
                del user_attempts[username]  # Reiniciar intentos en caso de éxito
            return redirect('home')  # Redirige a la página principal
        else:
            # Incrementar el contador de intentos fallidos
            attempts, lock_time = user_attempts.get(username, (0, None))
            attempts += 1

            if attempts >= 3:
                user_attempts[username] = (attempts, now())
                messages.error(request, 'Tu cuenta ha sido bloqueada por múltiples intentos fallidos.')
            else:
                user_attempts[username] = (attempts, lock_time)
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

    return render(request, 'login/login.html')  # Plantilla de inicio de sesión

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')  # Redirige a la vista de login

def home_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main_home')  # Redirige a la página principal
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

    return render(request, 'home.html', {'is_login_page': True})
