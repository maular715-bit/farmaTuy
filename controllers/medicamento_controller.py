from sqlalchemy.orm import Session
from sqlalchemy import select


from models.medicamento import Medicamento
#, TipoPrincipioActivo, TipoPresentacion 

# --- CRUD Functions ---

def get_medicamento(db: Session, medicamento_id: int) -> Medicamento | None:
    return db.scalar(
        select(Medicamento).filter(Medicamento.id == medicamento_id, Medicamento.estatus == True)
    )

def get_medicamentos(db: Session, skip: int = 0, limit: int = 100) -> list[Medicamento]:
    return list(
        db.scalars(
            select(Medicamento).filter(Medicamento.estatus == True).offset(skip).limit(limit)
        )
    )

def create_medicamento(db: Session, medicamento_data: dict) -> Medicamento:
    
    nuevo_medicamento = Medicamento(
        tipo_principio_activo_id=medicamento_data["tipo_principio_activo_id"],
        tipo_presentacion_id=medicamento_data["tipo_presentacion_id"],
        medicamento=medicamento_data["medicamento"],
        descripcion=medicamento_data.get("descripcion"),
        disposicion=medicamento_data.get("disposicion"),
        estatus=True
    )
    
    db.add(nuevo_medicamento)
    db.refresh(nuevo_medicamento)
    return nuevo_medicamento

def update_medicamento(db: Session, medicamento_id: int, medicamento_data: dict) -> Medicamento | None:
    medicamento_db = get_medicamento(db, medicamento_id)
    
    if medicamento_db:
        # Aplicar los cambios dinámicamente
        for key, value in medicamento_data.items():
            if key not in ['id', 'fecha_creacion'] and hasattr(medicamento_db, key) and value is not None:
                setattr(medicamento_db, key, value)
        db.commit()
        db.refresh(medicamento_db)
        return medicamento_db
    return None

def soft_delete_medicamento(db: Session, medicamento_id: int) -> bool:
    medicamento_db = get_medicamento(db, medicamento_id)
    
    if medicamento_db:
        medicamento_db.estatus = False
        db.commit()
        return True
    return False