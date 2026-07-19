from typing import Optional
from pydantic import BaseModel

class FarmaciaBase(BaseModel):
    nombre: str
    direccion: str
    telefono: str

class FarmaciaCreate(FarmaciaBase):
    pass

class Farmacia(FarmaciaBase):
    id: int
    estatus: Optional[str]
    class Config:
        orm_mode = True