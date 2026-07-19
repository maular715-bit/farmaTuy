from sqlalchemy import Column, Integer, String, DateTime, Boolean, UUID
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from database.db import Base 
class Responsable(Base):
    
    __tablename__ = 'responsables'

    id = Column(UUID, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    telefono = Column(String(50), nullable=True)
    correo = Column(String(255), unique=True, nullable=True)
    
    estatus = Column(Boolean, default=True) 
    fecha_creacion = Column(DateTime, default=datetime.now(timezone.utc))
    fecha_modificacion = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<Responsable(id={self.id}, nombre='{self.nombre}', apellido='{self.apellido}')>"