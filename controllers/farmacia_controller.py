from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from models.farmacia import Farmacia 


def get_farmacia(db: Session, farmacia_id: int) -> Farmacia | None:
    # Uso de .scalar() con select() es el estilo moderno de SQLAlchemy 2.0
    return db.scalar(
        select(Farmacia).filter(Farmacia.id == farmacia_id, Farmacia.estatus == True)
    )

def get_farmacias(db: Session, skip: int = 0, limit: int = 100) -> list[Farmacia]:
    return list(
        db.scalars(
            select(Farmacia).filter(Farmacia.estatus == True).offset(skip).limit(limit)
        )
    )

def create_farmacia(db: Session, farmacia_data: dict) -> Farmacia:
    nueva_farmacia = Farmacia(
        **farmacia_data,
        estatus=True,
        fecha_creacion=datetime.utcnow(),
        fecha_modificacion=datetime.utcnow()
    )
    
    db.add(nueva_farmacia)
    db.refresh(nueva_farmacia)
    return nueva_farmacia

def update_farmacia(db: Session, farmacia_id: int, farmacia_data: dict) -> Farmacia | None:
    farmacia_db = get_farmacia(db, farmacia_id)
    
    if farmacia_db:
        for key, value in farmacia_data.items():
            if key not in ['id', 'fecha_creacion'] and hasattr(farmacia_db, key) and value is not None:
                setattr(farmacia_db, key, value)
        db.commit()
        db.refresh(farmacia_db)
        return farmacia_db
    return None

def soft_delete_farmacia(db: Session, farmacia_id: int) -> bool:
    farmacia_db = get_farmacia(db, farmacia_id)
    
    if farmacia_db:
        farmacia_db.estatus = False
        db.commit()
        return True
    return False