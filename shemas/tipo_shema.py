from pydantic import BaseModel
from typing import Optional
class TipoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None   
class TipoCreate(TipoBase):
    pass
class Tipo(TipoBase):
    id: int
    estatus: Optional[bool] = True
    class Config:
        orm_mode = True
class TipoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estatus: Optional[bool] = None

