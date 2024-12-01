from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',  # Cambia la etiqueta del campo email
        }
        help_texts = {
            'username': None,  # Elimina el mensaje de ayuda de "150 caracteres como máximo..."
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_type']
        labels = {
            'user_type': 'Tipo de Empleado',  # Cambia la etiqueta de user_type
        }

class VerificationCodeForm(forms.Form):
    verification_code = forms.CharField(max_length=3, required=False, label='Código de Verificación')
