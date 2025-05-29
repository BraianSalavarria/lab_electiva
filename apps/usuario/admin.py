from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.usuario.models import Usuario
class UsuarioAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ['dni']}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ['dni']}),
    )
    filter_horizontal = ('groups', 'user_permissions')  # Esto habilita los selectores dobles

admin.site.register(Usuario, UsuarioAdmin)
