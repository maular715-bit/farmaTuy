from flask import Blueprint, request, jsonify
from database.db import get_db
from controllers import tipo_controller as service
from controllers.usuario_controller import token_required

tipo_bp = Blueprint("tipo", __name__)


def serialize_tipo(tipo_obj):
    return {
        "id": tipo_obj.id,
        "nombre": tipo_obj.nombre,
        "descripcion": tipo_obj.descripcion,
        "estatus": tipo_obj.estatus,
        "fecha_creacion": tipo_obj.fecha_creacion.isoformat() if tipo_obj.fecha_creacion else None,
        "fecha_modificacion": tipo_obj.fecha_modificacion.isoformat() if tipo_obj.fecha_modificacion else None,
    }


# --- CREATE ---
@tipo_bp.route("/", methods=["POST"])
@token_required
def create_tipo_route():
    data = request.get_json()
    required_fields = ["nombre"]
    if not data or not all(k in data for k in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    try:
        with get_db() as db:
            tipo = service.create_tipo(db, data)
            return jsonify(serialize_tipo(tipo)), 201
    except Exception as e:
        if 'duplicate key value violates unique constraint' in str(e):
            return jsonify({"error": "Ya existe un tipo con ese nombre"}), 409
        print(f"Error al crear tipo: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


# --- LIST ---
@tipo_bp.route("/", methods=["GET"])
def get_tipos_route():
    skip = request.args.get("skip", 0, type=int)
    limit = request.args.get("limit", 100, type=int)
    with get_db() as db:
        tipos = service.get_tipos(db, skip=skip, limit=limit)
        return jsonify([serialize_tipo(t) for t in tipos]), 200


# --- GET by ID ---
@tipo_bp.route("/<string:tipo_id>", methods=["GET"])
def get_tipo_by_id_route(tipo_id):
    with get_db() as db:
        tipo = service.get_tipo(db, tipo_id)
        if not tipo:
            return jsonify({"error": "Tipo no encontrado o inactivo"}), 404
        return jsonify(serialize_tipo(tipo)), 200


# --- UPDATE ---
@tipo_bp.route("/<string:tipo_id>", methods=["PUT"])
@token_required
def update_tipo_route(tipo_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos de actualización requeridos"}), 400

    try:
        with get_db() as db:
            updated = service.update_tipo(db, tipo_id, data)
            if not updated:
                return jsonify({"error": "Tipo no encontrado"}), 404
            return jsonify(serialize_tipo(updated)), 200
    except Exception as e:
        print(f"Error al actualizar tipo: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


# --- DELETE (soft) ---
@tipo_bp.route("/<string:tipo_id>", methods=["DELETE"])
@token_required
def delete_tipo_route(tipo_id):
    try:
        with get_db() as db:
            success = service.soft_delete_tipo(db, tipo_id)
            if not success:
                return jsonify({"error": "Tipo no encontrado o ya inactivo"}), 404
            return jsonify({"message": f"Tipo {tipo_id} desactivado correctamente"}), 200
    except Exception as e:
        print(f"Error al desactivar tipo: {e}")
        return jsonify({"error": "Error interno del servidor al desactivar"}), 500
