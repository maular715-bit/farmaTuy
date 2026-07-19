# controllers/farmacia_controller.py

from flask import Blueprint, request, jsonify
# Importamos la función get_db para el manejo de sesiones en la ruta
from database.db import get_db 
from controllers import farmacia_controller  as service 
# Asumo que tienes una función de seguridad como esta:
from controllers.usuario_controller import token_required 

farmacia_bp = Blueprint("farmacia", __name__)


def serialize_farmacia(farmacia_obj):
    return {
        "id": farmacia_obj.id,
        "razon_social": farmacia_obj.razon_social,
        "rif": farmacia_obj.rif,
        "estado": farmacia_obj.estado,
        "municipio": farmacia_obj.municipio,
        "parroquia": farmacia_obj.parroquia,
        "geo_ubicacion": farmacia_obj.geo_ubicacion,
        "telefono": farmacia_obj.telefono,
        "correo": farmacia_obj.correo,
        "estatus": farmacia_obj.estatus,
        "fecha_creacion": farmacia_obj.fecha_creacion.isoformat() if farmacia_obj.fecha_creacion else None,
        "fecha_modificacion": farmacia_obj.fecha_modificacion.isoformat() if farmacia_obj.fecha_modificacion else None,
    }

# --- 1. CREATE ---
@farmacia_bp.route("/", methods=["POST"])
# @token_required 
def create_farmacia_route():
    data = request.get_json()
    
    # Validación básica de campos obligatorios
    required_fields = ["razon_social", "rif", "estado", "municipio", "parroquia"]
    if not data or not all(k in data for k in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    try:
        # Usa get_db() para la sesión y transacción
        with get_db() as db:
            farmacia = service.create_farmacia(db, data)
            return jsonify(serialize_farmacia(farmacia)), 201
            
    except Exception as e:
        # Manejo de errores de unicidad (ej. rif ya existe)
        if 'duplicate key value violates unique constraint' in str(e):
             return jsonify({"error": "Razón social o RIF ya existe"}), 409
        print(f"Error al crear farmacia: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


# --- 2. READ (Lista) ---
@farmacia_bp.route("/", methods=["GET"])
def get_farmacias_route():
    skip = request.args.get("skip", 0, type=int)
    limit = request.args.get("limit", 100, type=int)
    
    with get_db() as db:
        farmacias = service.get_farmacias(db, skip=skip, limit=limit)
        return jsonify([serialize_farmacia(f) for f in farmacias]), 200

# --- 2. READ (Por ID) ---
@farmacia_bp.route("/<int:farmacia_id>", methods=["GET"])
def get_farmacia_by_id_route(farmacia_id):
    with get_db() as db:
        farmacia = service.get_farmacia(db, farmacia_id)
        if not farmacia:
            return jsonify({"error": "Farmacia no encontrada o inactiva"}), 404
        return jsonify(serialize_farmacia(farmacia)), 200


# --- 3. UPDATE ---
@farmacia_bp.route("/<int:farmacia_id>", methods=["PUT"])
# @token_required
def update_farmacia_route(farmacia_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos de actualización requeridos"}), 400
    
    try:
        with get_db() as db:
            updated_farmacia = service.update_farmacia(db, farmacia_id, data)
            if not updated_farmacia:
                return jsonify({"error": "Farmacia no encontrada"}), 404
            return jsonify(serialize_farmacia(updated_farmacia)), 200
            
    except Exception as e:
        print(f"Error al actualizar farmacia: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


# --- 4. DELETE (Lógica) ---
@farmacia_bp.route("/<int:farmacia_id>", methods=["DELETE"])
# @token_required
def delete_farmacia_route(farmacia_id):
    try:
        with get_db() as db:
            success = service.soft_delete_farmacia(db, farmacia_id)
            if not success:
                return jsonify({"error": "Farmacia no encontrada o ya inactiva"}), 404
            
            return jsonify({"message": f"Farmacia {farmacia_id} desactivada correctamente"}), 200
            
    except Exception as e:
        print(f"Error al desactivar farmacia: {e}")
        return jsonify({"error": "Error interno del servidor al desactivar"}), 500