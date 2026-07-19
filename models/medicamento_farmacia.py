from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from database.db import Base 
class InventarioFarmacia(Base):
    
    __tablename__ = 'medicamento_farmacia'

    id = Column(Integer, primary_key=True, index=True)
    farmacia_id = Column(Integer, nullable=False)  # ID de la farmacia
    medicamento_id = Column(Integer, nullable=False)  # ID del medicamento
    cantidad = Column(Integer, default=0)  # Cantidad en inventario
    
    estatus = Column(Boolean, default=True) 
    fecha_creacion = Column(DateTime, default=datetime.now(timezone.utc))
    fecha_modificacion = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    medicamento = relationship("Medicamento", back_populates="farmacias")
    def __repr__(self):
        return f"<InventarioFarmacia(id={self.id}, farmacia_id={self.farmacia_id}, medicamento_id={self.medicamento_id}, cantidad={self.cantidad})>"    
    