from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from models.tipo import Tipo


def get_tipo(db: Session, tipo_id: str) -> Tipo | None:
    return db.scalar(
        select(Tipo).filter(Tipo.id == tipo_id, Tipo.estatus == True)
    )


def get_tipos(db: Session, skip: int = 0, limit: int = 100) -> list[Tipo]:
    return list(
        db.scalars(
            select(Tipo).filter(Tipo.estatus == True).offset(skip).limit(limit)
        )
    )


def create_tipo(db: Session, tipo_data: dict) -> Tipo:
    nueva = Tipo(
        **tipo_data,
        estatus=True,
        fecha_creacion=datetime.utcnow(),
        fecha_modificacion=datetime.utcnow()
    )
    db.add(nueva)
    db.refresh(nueva)
    return nueva


def update_tipo(db: Session, tipo_id: str, tipo_data: dict) -> Tipo | None:
    tipo_db = get_tipo(db, tipo_id)
    if tipo_db:
        for key, value in tipo_data.items():
            if key not in ['id', 'fecha_creacion'] and hasattr(tipo_db, key) and value is not None:
                setattr(tipo_db, key, value)
        db.commit()
        db.refresh(tipo_db)
        return tipo_db
    return None


def soft_delete_tipo(db: Session, tipo_id: str) -> bool:
    tipo_db = get_tipo(db, tipo_id)
    if tipo_db:
        tipo_db.estatus = False
        db.commit()
        return True
    return False
