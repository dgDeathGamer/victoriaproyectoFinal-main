# usuarios/models.py
from datetime import timezone
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('jefe', 'Jefe'),
        ('empleado', 'Empleado'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con el modelo de usuario
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)  # Tipo de usuario (jefe o empleado)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Número de teléfono opcional
    email = models.EmailField(max_length=255, blank=True, null=True)  # Correo electrónico opcional
   
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"  # Representación del objeto

    def get_full_name(self):
        # Método para obtener el nombre completo del usuario
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"
