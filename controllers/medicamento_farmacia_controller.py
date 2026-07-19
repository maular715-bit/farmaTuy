from sqlalchemy.orm import Session
from sqlalchemy import select

from models.medicamento_farmacia import InventarioFarmacia
# --- CRUD Functions ---
def get_inventario_farmacia(db: Session, inventario_id: int) -> InventarioFarmacia | None:
    return db.scalar(
        select(InventarioFarmacia).filter(InventarioFarmacia.id == inventario_id, InventarioFarmacia.estatus == True)
    )
def get_inventarios_farmacia(db: Session, skip: int = 0, limit: int = 100) -> list[InventarioFarmacia]:
    return list(
        db.scalars(
            select(InventarioFarmacia).filter(InventarioFarmacia.estatus == True).offset(skip).limit(limit)
        )
    )
def create_inventario_farmacia(db: Session, inventario_data: dict) -> InventarioFarmacia:
    
    nuevo_inventario = InventarioFarmacia(
        farmacia_id=inventario_data["farmacia_id"],
        medicamento_id=inventario_data["medicamento_id"],
        cantidad=inventario_data.get("cantidad", 0),
        estatus=True
    )
    
    db.add(nuevo_inventario)
    db.refresh(nuevo_inventario)
    return nuevo_inventario
def update_inventario_farmacia(db: Session, inventario_id: int, inventario_data: dict) -> InventarioFarmacia | None:
    inventario_db = get_inventario_farmacia(db, inventario_id)
    
    if inventario_db:
        # Aplicar los cambios dinámicamente
        for key, value in inventario_data.items():
            if key not in ['id', 'fecha_creacion'] and hasattr(inventario_db, key) and value is not None:
                setattr(inventario_db, key, value)
        db.commit()
        db.refresh(inventario_db)
        return inventario_db
    return None
def soft_delete_inventario_farmacia(db: Session, inventario_id: int) -> bool:
    inventario_db = get_inventario_farmacia(db, inventario_id)
    
    if inventario_db:
        inventario_db.estatus = False
        db.commit()
        return True
    return False


