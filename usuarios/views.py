from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, UserProfileForm, VerificationCodeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def add_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        verification_code_form = VerificationCodeForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Validar el código de verificación si el usuario es jefe
            if profile.user_type == 'jefe':
                verification_code = verification_code_form.cleaned_data.get('verification_code')
                if verification_code != '123':
                    messages.error(request, 'El código de verificación es incorrecto.')
                    return render(request, 'usuarios/add_user.html', {
                        'user_form': user_form,
                        'profile_form': profile_form,
                        'verification_code_form': verification_code_form,
                    })
            
            messages.success(request, 'Usuario agregado exitosamente.')
            return redirect('usuarios')  # Redirige a la vista de lista de usuarios

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        verification_code_form = VerificationCodeForm()
    
    return render(request, 'usuarios/add_user.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'verification_code_form': verification_code_form,
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                user_profile = UserProfile.objects.get(user=user)  # Obtener el perfil de usuario

                # Redirigir a la vista del panel correspondiente
                if user_profile.user_type == 'jefe':
                    messages.success(request, 'Bienvenido, Jefe.')
                    return redirect('boss_panel')  # URL del panel de jefe
                else:
                    messages.success(request, 'Bienvenido, Empleado.')
                    return redirect('employee_panel')  # URL del panel de empleado
            except UserProfile.DoesNotExist:
                messages.error(request, 'Perfil de usuario no encontrado.')
                return redirect('login')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

    return render(request, 'login/login.html')

@login_required
def employee_panel(request):
    # Verifica si el usuario tiene el rol adecuado
    if request.user.is_authenticated and request.user.userprofile.user_type == 'empleado':
        return render(request, 'usuarios/employee_panel.html')  # Plantilla para empleados
    else:
        return redirect('home')  # Redirigir si no tiene permiso

@login_required
def boss_panel(request):
    # Verifica si el usuario tiene el rol adecuado
    if request.user.is_authenticated and request.user.userprofile.user_type == 'jefe':
        return render(request, 'usuarios/boss_panel.html')  # Plantilla para jefes
    else:
        return redirect('home')  # Redirigir si no tiene permiso

@login_required
def reportes_view(request):
    # Lógica de la vista para los reportes
    return render(request, 'usuarios/reportes.html')

@login_required
def usuarios_view(request):
    # Obtener todos los usuarios que no son superusuarios
    users = User.objects.filter(is_superuser=False)
    return render(request, 'usuarios/usuarios.html', {'users': users})

@login_required
def edit_user(request, user_id):
    # Obtener el usuario y el perfil a editar
    user = get_object_or_404(User, pk=user_id, is_superuser=False)
    profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('usuarios')  # Redirigir a la lista de usuarios

    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'usuarios/edit_user.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_id': user_id
    })

@login_required
def delete_user(request, user_id):
    # Obtener el usuario a eliminar
    user = get_object_or_404(User, pk=user_id, is_superuser=False)

    if request.method == 'POST':
        username = user.username  # Obtener el nombre del usuario antes de eliminarlo
        user.delete()
        messages.success(request, f'Usuario {username} eliminado exitosamente.')
        return redirect('usuarios')  # Redirigir a la lista de usuarios

    return render(request, 'usuarios/confirm_delete.html', {'user': user})
