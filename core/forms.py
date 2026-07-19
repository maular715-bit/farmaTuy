from django import forms
from .models import Farmacia, Medicamento, InventarioFarmacia, Tipo, Usuario, AuthUsuario


class FarmaciaForm(forms.ModelForm):
    class Meta:
        model = Farmacia
        fields = ['razon_social', 'rif', 'estado', 'municipio', 'parroquia', 'geo_ubicacion', 'telefono', 'correo']


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['medicamento', 'descripcion', 'disposicion', 'tipo_principio_activo', 'tipo_presentacion']


class InventarioForm(forms.ModelForm):
    class Meta:
        model = InventarioFarmacia
        fields = ['farmacia', 'medicamento', 'cantidad']


class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['nombre', 'descripcion']


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'auth_usuario', 'tipo']
