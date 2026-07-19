import os
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt
from functools import wraps
from flask import Blueprint, request, jsonify, g
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.db import get_db
from models.usuario import AuthUsuario, Usuario 
from shemas import usuario_shema as schemas
from controllers.auth_controller import hash_password
usuario_bp = Blueprint("usuario", __name__)

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXP_SECONDS = int(os.getenv("JWT_EXP_SECONDS", "3600"))

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing or invalid"}), 401
        token = auth_header.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        g.current_user = {
            "id": payload.get("sub"),
            "username": payload.get("username"),
            "email": payload.get("email")
        }
        return f(*args, **kwargs)
    return decorated

@usuario_bp.route("/register", methods=["POST"])
def register(db, usuario_data):

    username = (usuario_data.get("username") or "").strip() 
    email = (usuario_data.get("email") or "").strip().lower() 
    password_hash = usuario_data.get("password") or ""
    print(username)
    if not username or not email or not password_hash:
        raise ValueError("username, email and password are required")
        pass
    password_bytes = password_hash.encode("utf-8")
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt).decode("utf-8")
    stmt_email = select(AuthUsuario).filter_by(correo=email)
    existing_auth_user = db.scalar(stmt_email) 
    stmt_username = select(Usuario).filter_by(username=username)
    existing_user = db.scalar(stmt_username) 

    if existing_auth_user or existing_user:
        raise ValueError("Ya existe un usuario con ese correo o nombre de usuario")
            # 3. Crear AuthUsuario
    new_auth_user = AuthUsuario(
        correo=email,
        password_hash=password_hash,
        fecha_creacion=datetime.now(timezone.utc)
        )
    db.add(new_auth_user)
    db.flush() # Necesario para obtener new_auth_user.id
            
    new_user = Usuario(
        auth_usuario_id=new_auth_user.id, 
        username=username,
        estatus=True,
        fecha_creacion=datetime.now(timezone.utc)
    )
    db.add(new_user)
    return new_user
           

@usuario_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "correo y contrasena es requerido"}), 400
    
    user_info = None
    
    try:
        with get_db() as db:
            # 1. Buscar AuthUsuario por correo (email)
            auth_user = db.scalar(
                select(AuthUsuario).filter_by(correo=email)
            )
            
            if not auth_user:
                return jsonify({"error": "Invalidas credentiales"}), 401
            
            # 2. Verificar la contraseña
            stored_hash = auth_user.password_hash
            if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
                return jsonify({"error": "Invalidas credentiales"}), 401

            # 3. Obtener el Username de la tabla 'usuario' a través de la relación
            user = db.scalar(
                select(Usuario).filter_by(auth_usuario_id=auth_user.id)
            )
            
            if not user:
                 return jsonify({"error": "User profile missing"}), 500
                 
            user_info = {
                "id": auth_user.id,
                "username": user.username,
                "email": auth_user.correo
            }
            
        # 4. Generación del Token 
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_info["id"],
            "username": user_info["username"],
            "email": user_info["email"],
            "iat": now,
            "exp": now + datetime.timedelta(seconds=JWT_EXP_SECONDS)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
    except Exception as e:
        print(f"Error durante el login: {e}")
        return jsonify({"error": "Internal server error during login"}), 500
    
    return jsonify({"access_token": token, "token_type": "Bearer", "expires_in": JWT_EXP_SECONDS})

@usuario_bp.route("/me", methods=["GET"])
@token_required
def me():
    user = g.get("current_user")
    return jsonify({"user": user})


def crear_usuario(db: Session, usuario: schemas.UsuarioCreate): 
    
    hashed_pw = hash_password(usuario.password)
    nuevo = AuthUsuario(
        correo=usuario.correo,
        nombre_primero=usuario.nombre_primero,
        apellido_paterno=usuario.apellido_paterno,
        estatus=True, 
        fecha_creacion=datetime.now(timezone.utc),
        fecha_modificacion=datetime.now(timezone.utc),
        password_hash=hashed_pw  
    )
    db.add(nuevo)
    db.refresh(nuevo)
    

    new_user_profile = Usuario(auth_usuario_id=nuevo.id, username=...)
    db.add(new_user_profile)
    db.refresh(new_user_profile)
    
    return nuevo