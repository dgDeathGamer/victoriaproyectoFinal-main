from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type')  # Campos a mostrar en la lista

admin.site.register(UserProfile, UserProfileAdmin)
