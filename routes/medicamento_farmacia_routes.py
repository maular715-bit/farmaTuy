from flask import Blueprint, request, jsonify
from database.db import get_db
from controllers import medicamento_farmacia_controller as service
from controllers.usuario_controller import token_required
medicamento_farmacia_bp = Blueprint("medicamento_farmacia", __name__)
def serialize_medicamento_farmacia(medicamento_farmacia_obj):
    return {
        "id": medicamento_farmacia_obj.id,
        "farmacia_id": medicamento_farmacia_obj.farmacia_id,
        "medicamento_id": medicamento_farmacia_obj.medicamento_id,
        "cantidad": medicamento_farmacia_obj.cantidad,
        "estatus": medicamento_farmacia_obj.estatus,
        "fecha_creacion": medicamento_farmacia_obj.fecha_creacion.isoformat(),
        "fecha_modificacion": medicamento_farmacia_obj.fecha_modificacion.isoformat(),
    }
# --- 1. CREATE ---
@medicamento_farmacia_bp.route("/", methods=["POST"])
@token_required
def create_medicamento_farmacia_route():
    data = request.get_json()
    
    required_fields = ["farmacia_id", "medicamento_id", "cantidad"]
    if not data or not all(k in data for k in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    try:
        with get_db() as db:
            medicamento_farmacia = service.create_medicamento_farmacia(db, data)
            return jsonify(serialize_medicamento_farmacia(medicamento_farmacia)), 201
            
    except Exception as e:
        if 'violates foreign key constraint' in str(e):
             return jsonify({"error": "ID de farmacia o medicamento inválido"}), 400
        
        print(f"Error al crear medicamento en farmacia: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
# --- 2. READ (Lista) ---
@medicamento_farmacia_bp.route("/", methods=["GET"])
def get_medicamento_farmacias_route():
    skip = request.args.get("skip", 0, type=int)
    limit = request.args.get("limit", 100, type=int)
    try:
        with get_db() as db:
            medicamento_farmacias = service.get_medicamento_farmacias(db, skip=skip, limit=limit)
            serialized = [serialize_medicamento_farmacia(mf) for mf in medicamento_farmacias]
            return jsonify(serialized), 200
    except Exception as e:
        print(f"Error al obtener medicamentos en farmacias: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
    try:
        with get_db() as db:
            medicamento_farmacia = service.get_medicamento_farmacia(db, medicamento_farmacia_id)
            if medicamento_farmacia:
                return jsonify(serialize_medicamento_farmacia(medicamento_farmacia)), 200
            else:
                return jsonify({"error": "Medicamento en farmacia no encontrado"}), 404
    except Exception as e:
        print(f"Error al obtener medicamento en farmacia: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
    
   
# --- 2. READ (Por ID) ---
@medicamento_farmacia_bp.route("/<int:medicamento_farmacia_id>", methods=["GET"])
def get_medicamento_farmacia_by_id_route(medicamento_farmacia_id):
    try:
        with get_db() as db:
            medicamento_farmacia = service.get_medicamento_farmacia(db, medicamento_farmacia_id)
            if medicamento_farmacia:
                return jsonify(serialize_medicamento_farmacia(medicamento_farmacia)), 200
            else:
                return jsonify({"error": "Medicamento en farmacia no encontrado"}), 404
    except Exception as e:
        print(f"Error al obtener medicamento en farmacia: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
# --- 3. UPDATE ---
@medicamento_farmacia_bp.route("/<int:medicamento_farmacia_id>", methods=["PUT"])
@token_required             
def update_medicamento_farmacia_route(medicamento_farmacia_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos de actualización requeridos"}), 400
    
    try:
        with get_db() as db:
            medicamento_farmacia = service.update_medicamento_farmacia(db, medicamento_farmacia_id, data)
            if medicamento_farmacia:
                return jsonify(serialize_medicamento_farmacia(medicamento_farmacia)), 200
            else:
                return jsonify({"error": "Medicamento en farmacia no encontrado"}), 404 
    except Exception as e:
        print(f"Error al actualizar medicamento en farmacia: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
# --- 4. DELETE (Lógica) ---
@medicamento_farmacia_bp.route("/<int:medicamento_farmacia_id>", methods=["DELETE"])
@token_required
def delete_medicamento_farmacia_route(medicamento_farmacia_id):
    try:
        with get_db() as db:
            success = service.soft_delete_medicamento_farmacia(db, medicamento_farmacia_id)
            if success:
                return jsonify({"message": f"Medicamento en farmacia {medicamento_farmacia_id} desactivado correctamente"}), 200
            else:
                return jsonify({"error": "Medicamento en farmacia no encontrado o ya inactivo"}), 404
    except Exception as e:
        print(f"Error al desactivar medicamento en farmacia: {e}")
        return jsonify({"error": "Error interno del servidor al desactivar"}), 500
    
