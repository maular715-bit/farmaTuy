from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager
import controllers.usuario_controller  as crud
from sqlalchemy.orm import Session
from flask import Blueprint, request, jsonify,  current_app
from database.db import get_db 
usuario_bp = Blueprint("usuario", __name__)

def serialize_usuario(usuario_obj):
    return{
        "username": usuario_obj.username,
        "email": usuario_obj.email,
        "password": usuario_obj.password
    }

# Archivo donde está la ruta

@usuario_bp.route("/", methods=["POST"])
def registrar_usuario():
    data = request.get_json()
    required_fields = ["username", "email", "password"]
    if not data or not all(k in data for k in required_fields):
        return jsonify({"error": "Se requieren los campos: username, email y password"}), 400

    usuario_data = dict(data)
    
    try:
        with get_db() as db_usu:
            new_user = crud.register(db_usu, usuario_data) 
        return jsonify(serialize_usuario(new_user)), 201 
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
        
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@usuario_bp.route("/login", methods=["POST"])
def login_usuario(usuario=None, db=None):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"msg": "Se requiere un cuerpo JSON"}), 400
    usuario = dict(data)
    if db is None:
        db = getattr(current_app, "db", None)
    if db is None:
        return jsonify({"msg": "Sesión de base de datos no disponible"}), 500
    return crud.autenticar_usuario(db, usuario)
@usuario_bp.route("/protected", methods=["GET"])
def protected_route(db=None):
    if db is None:
        db = getattr(current_app, "db", None)
    if db is None:
        return jsonify({"msg": "Sesión de base de datos no disponible"}), 500
    return crud.ruta_protegida(db)
@usuario_bp.route("/users", methods=["GET"])
def listar_usuarios(db=None):
    if db is None:
        db = getattr(current_app, "db", None)
    if db is None:
        return jsonify({"msg": "Sesión de base de datos no disponible"}), 500
    return crud.obtener_usuarios(db)
@usuario_bp.route("/users/<int:user_id>", methods=["GET"])
def obtener_usuario(user_id, db=None):
    if db is None:
        db = getattr(current_app, "db", None)
    if db is None:
        return jsonify({"msg": "Sesión de base de datos no disponible"}), 500
    return crud.obtener_usuario_por_id(db, user_id)
@usuario_bp.route("/users/<int:user_id>", methods=["PUT"])
def actualizar_usuario(user_id, db=None):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"msg": "Se requiere un cuerpo JSON"}), 400
    usuario = dict(data)
    if "password" in usuario and usuario["password"]:
        usuario["password"] = generate_password_hash(usuario["password"])
    if db is None:
        db = getattr(current_app, "db", None)
    if db is None:
        return jsonify({"msg": "Sesión de base de datos no disponible"}), 500
    return crud.actualizar_usuario(db, user_id, usuario)
@usuario_bp.route("/users/<int:user_id>", methods=["DELETE"])
def eliminar_usuario(user_id, db=None):
    if db is None:
        db = getattr(current_app, "db", None)
    if db is None:
        return jsonify({"msg": "Sesión de base de datos no disponible"}), 500
    return crud.eliminar_usuario(db, user_id)
