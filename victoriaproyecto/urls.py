# urls.py
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from login.views import home_view  # Importa la vista de inicio

urlpatterns = [
    path('admin/', admin.site.urls),  # URL para el panel de administración
    path('', home_view, name='home'),  # Página de inicio de la aplicación
    path('login/', include('login.urls')),  # Incluye las URLs de la aplicación de login
    path('usuarios/', include('usuarios.urls')),  # Incluye las URLs de la aplicación de usuarios
    path('inventario/', include('inventario.urls')),  # Incluye las URLs de la aplicación de inventario
    path('ventas/', include('ventas.urls')),  # Incluye las URLs de la aplicación de ventas
    path('reportes/', include('reportes.urls')),  # Incluye las URLs de la aplicación de reportes
]

# Configuración para servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
