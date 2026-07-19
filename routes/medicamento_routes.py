from flask import Blueprint, request, jsonify
from database.db import get_db 
from controllers import medicamento_controller as service 
from controllers.usuario_controller import token_required 

medicamento_bp = Blueprint("medicamento", __name__)

def serialize_medicamento(medicamento_obj):
   
    return {
        "id": medicamento_obj.id,
        "medicamento": medicamento_obj.medicamento,
        "descripcion": medicamento_obj.descripcion,
        "disposicion": medicamento_obj.disposicion,
        
        "principio_activo": {
            "id": medicamento_obj.principio_activo.id,
            "nombre": medicamento_obj.principio_activo.nombre,
        } if medicamento_obj.principio_activo else None,
        "presentacion": {
            "id": medicamento_obj.presentacion.id,
            "nombre": medicamento_obj.presentacion.nombre,
        } if medicamento_obj.presentacion else None,
        
        "estatus": medicamento_obj.estatus,
        "fecha_creacion": medicamento_obj.fecha_creacion.isoformat(),
        "fecha_modificacion": medicamento_obj.fecha_modificacion.isoformat(),
    }

# --- 1. CREATE ---
@medicamento_bp.route("/", methods=["POST"])
@token_required 
def create_medicamento_route():
    data = request.get_json()
    
    required_fields = ["medicamento", "tipo_principio_activo_id", "tipo_presentacion_id"]
    if not data or not all(k in data for k in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    try:
        with get_db() as db:
            medicamento = service.create_medicamento(db, data)
            return jsonify(serialize_medicamento(medicamento)), 201
            
    except Exception as e:
        if 'violates foreign key constraint' in str(e):
             return jsonify({"error": "ID de principio activo o presentación inválido"}), 400
        if 'duplicate key value violates unique constraint' in str(e):
             return jsonify({"error": "Ya existe un medicamento con ese nombre"}), 409
        
        print(f"Error al crear medicamento: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


# --- 2. READ (Lista) ---
@medicamento_bp.route("/", methods=["GET"])
def get_medicamentos_route():
    skip = request.args.get("skip", 0, type=int)
    limit = request.args.get("limit", 100, type=int)
    
    with get_db() as db:
        medicamentos = service.get_medicamentos(db, skip=skip, limit=limit)
        return jsonify([serialize_medicamento(m) for m in medicamentos]), 200

# --- 2. READ (Por ID) ---
@medicamento_bp.route("/<int:medicamento_id>", methods=["GET"])
def get_medicamento_by_id_route(medicamento_id):
    with get_db() as db:
        medicamento = service.get_medicamento(db, medicamento_id)
        if not medicamento:
            return jsonify({"error": "Medicamento no encontrado o inactivo"}), 404
        return jsonify(serialize_medicamento(medicamento)), 200


# --- 3. UPDATE ---
@medicamento_bp.route("/<int:medicamento_id>", methods=["PUT"])
@token_required
def update_medicamento_route(medicamento_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos de actualización requeridos"}), 400
    
    try:
        with get_db() as db:
            updated_medicamento = service.update_medicamento(db, medicamento_id, data)
            if not updated_medicamento:
                return jsonify({"error": "Medicamento no encontrado"}), 404
            return jsonify(serialize_medicamento(updated_medicamento)), 200
            
    except Exception as e:
        print(f"Error al actualizar medicamento: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


# --- 4. DELETE (Lógica) ---
@medicamento_bp.route("/<int:medicamento_id>", methods=["DELETE"])
@token_required
def delete_medicamento_route(medicamento_id):
    try:
        with get_db() as db:
            success = service.soft_delete_medicamento(db, medicamento_id)
            if not success:
                return jsonify({"error": "Medicamento no encontrado o ya inactivo"}), 404
            
            return jsonify({"message": f"Medicamento {medicamento_id} desactivado correctamente"}), 200
            
    except Exception as e:
        print(f"Error al desactivar medicamento: {e}")
        return jsonify({"error": "Error interno del servidor al desactivar"}), 500