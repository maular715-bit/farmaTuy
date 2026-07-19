from django.contrib import admin
from .models import Tipo, Farmacia, Medicamento, AuthUsuario, Usuario, InventarioFarmacia

@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estatus')


@admin.register(Farmacia)
class FarmaciaAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'rif', 'correo', 'estatus')


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('medicamento', 'tipo_principio_activo', 'tipo_presentacion', 'estatus')


@admin.register(AuthUsuario)
class AuthUsuarioAdmin(admin.ModelAdmin):
    list_display = ('correo', 'nombre_primero', 'estatus')


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'auth_usuario', 'estatus')


@admin.register(InventarioFarmacia)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('farmacia', 'medicamento', 'cantidad', 'estatus')
