from django.urls import path
from .views import login_view, logout_view, home_view  # Importa las vistas necesarias

urlpatterns = [
    path('', login_view, name='login'),  # Vista de inicio de sesión
    path('logout/', logout_view, name='logout'),  # Vista para cerrar sesión
    path('home/', home_view, name='home'),  # Vista para la página de inicio, si la necesitas aquí
]
