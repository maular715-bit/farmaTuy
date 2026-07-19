from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    correo: str
    nombre_primero: str
    apellido_paterno: str

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int
    estatus: Optional[str]
    class Config:
        orm_mode = True