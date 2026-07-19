import uuid
from django.db import models


class Tipo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estatus = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Farmacia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    razon_social = models.CharField(max_length=255, unique=True)
    rif = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    parroquia = models.CharField(max_length=100)
    geo_ubicacion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    correo = models.EmailField(max_length=255, null=True, blank=True, unique=True)
    estatus = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.razon_social


class Medicamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo_principio_activo = models.ForeignKey(Tipo, related_name='medicamentos_principio_activo', on_delete=models.PROTECT)
    tipo_presentacion = models.ForeignKey(Tipo, related_name='medicamentos_presentacion', on_delete=models.PROTECT)
    medicamento = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    disposicion = models.CharField(max_length=255, null=True, blank=True)
    estatus = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.medicamento


class AuthUsuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_primero = models.CharField(max_length=255, null=True, blank=True)
    apellido_paterno = models.CharField(max_length=255, null=True, blank=True)
    correo = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    estatus = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)


class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auth_usuario = models.OneToOneField(AuthUsuario, related_name='usuario', on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    tipo = models.ForeignKey(Tipo, null=True, blank=True, on_delete=models.SET_NULL)
    # Roles: farmacia_responsable can manage own farmacia and its medicamentos
    # supervisor can manage users and farmacias
    # externo is public read-only
    ROLE_FARMACIA = 'farmacia_responsable'
    ROLE_SUPERVISOR = 'supervisor'
    ROLE_EXTERNO = 'externo'
    ROLE_CHOICES = [
        (ROLE_FARMACIA, 'Farmacia responsable'),
        (ROLE_SUPERVISOR, 'Supervisor'),
        (ROLE_EXTERNO, 'Externo'),
    ]
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default=ROLE_FARMACIA)
    estatus = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class InventarioFarmacia(models.Model):
    id = models.AutoField(primary_key=True)
    farmacia = models.ForeignKey(Farmacia, related_name='inventario', on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, related_name='farmacias', on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    estatus = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.farmacia} - {self.medicamento} ({self.cantidad})"


class BlacklistedToken(models.Model):
    token = models.TextField(unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BlacklistedToken(id={self.id})"
