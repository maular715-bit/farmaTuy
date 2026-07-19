from sqlalchemy import Column, Integer, String, DateTime, Boolean, UUID
from datetime import datetime, timezone
from database.db import Base 

class Farmacia(Base):
   
    __tablename__ = 'farmacia'

    id = Column(UUID, primary_key=True, index=True)
    razon_social = Column(String(255), unique=True, nullable=False)
    rif = Column(String(50), unique=True, nullable=False)
    estado = Column(String(100), nullable=False)
    municipio = Column(String(100), nullable=False)
    parroquia = Column(String(100), nullable=False)
    geo_ubicacion = Column(String(255), nullable=True)
    telefono = Column(String(50), nullable=True)
    correo = Column(String(255), unique=True, nullable=True)
    
    estatus = Column(Boolean, default=True) # Uso de booleano
    fecha_creacion = Column(DateTime,default=datetime.now(timezone.utc))
    fecha_modificacion = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<Farmacia(id={self.id}, razon_social='{self.razon_social}')>"