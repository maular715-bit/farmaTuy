from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class MedicamentoBase(BaseModel):
    Medicamento: str
    descripcion: Optional[str]
    disposicion: Optional[str]
    tipo_principio_activo_id: int
    tipo_presentacion_id: int

class MedicamentoCreate(MedicamentoBase):
    pass

class Medicamento(MedicamentoBase):
    id: UUID
    estatus: Optional[str]

    class Config:
        orm_mode = True