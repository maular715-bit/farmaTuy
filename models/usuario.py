from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.db import Base 
from models.tipo import Tipo

# Modelo para la tabla 'auth_usuario' (datos personales y hash de contraseña)
class AuthUsuario(Base):
    __tablename__ = 'auth_usuario'

    id = Column(UUID, primary_key=True, index=True)
    nombre_primero = Column(String, nullable=True)
    apellido_paterno = Column(String, nullable=True)
    correo = Column(String, unique=True, index=True, nullable=False) # Usado para login
    password_hash = Column(String, nullable=False) # Almacena el hash de la contraseña
    estatus = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.now(timezone.utc))
    fecha_modificacion = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    # Relación con la tabla 'usuario'
    usuario = relationship("Usuario", back_populates="auth_usuario", uselist=False)

# Modelo para la tabla 'usuario' (relación con tipos y roles)
class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(UUID, primary_key=True, index=True)
    # Columna foránea que apunta a AuthUsuario
    auth_usuario_id = Column(UUID, ForeignKey('auth_usuario.id'), unique=True, nullable=False)
    
    username = Column(String(150), unique=True, index=True, nullable=False) # Asumiendo que el campo 'usuario' del diagrama es el username
    
    tipo_usuario_id = Column(UUID, ForeignKey('tipos.id'), nullable=True) 

    estatus = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.now(timezone.utc))
    fecha_modificacion = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    # Relaciones
    auth_usuario = relationship("AuthUsuario", back_populates="usuario")
    tipo = relationship(
        "Tipo", 
        foreign_keys=[tipo_usuario_id] ,
        remote_side=[Tipo.id]
    )
    def __repr__(self):
        return f"<Usuario(id={self.id}, username='{self.username}')>"