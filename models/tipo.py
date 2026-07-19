from sqlalchemy import Column, Integer, String, DateTime, Boolean, UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.db import Base 

class Tipo(Base):
    __tablename__ = 'tipos' 

    id = Column(UUID, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(String, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.now(timezone.utc))
    fecha_modificacion = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    estatus = Column(Boolean, default=True) 
    def __repr__(self):
        return f"<Tipo(id={self.id}, nombre='{self.nombre}')>"

    medicamentos_principio_activo = relationship("Medicamento", back_populates="tipo_principio_activo", foreign_keys='Medicamento.tipo_principio_activo_id')
    medicamentos_presentacion = relationship("Medicamento", back_populates="tipo_presentacion", foreign_keys='Medicamento.tipo_presentacion_id')
    usuarios = relationship("Usuario", back_populates="tipo_usuario", foreign_keys='Usuario.tipo_usuario_id')