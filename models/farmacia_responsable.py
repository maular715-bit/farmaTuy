from sqlalchemy import Column, Integer, String, DateTime, Boolean, UUID
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from database.db import Base 
class farmacia_responsable(Base):
    
    __tablename__ = 'farmacia_responsable'

    id = Column(UUID, primary_key=True, index=True)
    farmacia_id = Column(Integer, nullable=False)  # ID de la farmacia
    responsable_id = Column(Integer, nullable=False)  # ID del responsable
    
    estatus = Column(Boolean, default=True) 
    fecha_creacion = Column(DateTime, default=datetime.now(timezone.utc))
    fecha_modificacion = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<FarmaciaResponsable(id={self.id}, farmacia_id={self.farmacia_id}, responsable_id={self.responsable_id})>"