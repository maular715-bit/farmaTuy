from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.db import Base 
from models.tipo import Tipo
class Medicamento(Base):
    
    __tablename__ = 'medicamentos'

    id = Column(UUID, primary_key=True, index=True)
    
    tipo_principio_activo_id = Column(UUID, ForeignKey('tipos.id'), nullable=False)
    tipo_presentacion_id = Column(UUID, ForeignKey('tipos.id'), nullable=False)
    
    medicamento = Column(String(255), unique=True, nullable=False) # Nombre del medicamento
    descripcion = Column(String(500), nullable=True)
    disposicion = Column(String(255), nullable=True) # Ej: "Bajo prescripción", "Venta libre"
    
    estatus = Column(Boolean, default=True) 
    fecha_creacion = Column(DateTime, default=datetime.now(timezone.utc))
    fecha_modificacion = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    principio_activo = relationship(
        "Tipo", 
        foreign_keys=[tipo_principio_activo_id] ,
        remote_side=[Tipo.id]
    )
    
    presentacion = relationship(
        "Tipo",
        foreign_keys=[tipo_presentacion_id] ,
         remote_side=[Tipo.id]
    )
    
    farmacias = relationship("InventarioFarmacia", back_populates="medicamento")
    def __repr__(self):
        return f"<Medicamento(id={self.id}, medicamento='{self.medicamento}')>"