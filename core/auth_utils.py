import os
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt

SECRET_KEY = os.getenv('JWT_SECRET', 'change-me')
ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('JWT_EXP_MINUTES', '60'))

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


# Blacklist utilities (requires core.models.BlacklistedToken)
def is_token_blacklisted(token: str) -> bool:
    try:
        from .models import BlacklistedToken
        return BlacklistedToken.objects.filter(token=token).exists()
    except Exception:
        return False


def blacklist_token(token: str) -> None:
    try:
        from .models import BlacklistedToken
        BlacklistedToken.objects.get_or_create(token=token)
    except Exception:
        pass


from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def error_response(code: str, message: str, details: dict | None = None, http_status: int = status.HTTP_400_BAD_REQUEST) -> Response:
    payload = {
        "error": {
            "code": code,
            "message": message,
        }
    }
    if details is not None:
        payload["error"]["details"] = details
    return Response(payload, status=http_status)


def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped(*f_args, **kwargs):
        # Support decorating both function-based views and class methods
        # Find the request object among positional args
        request = None
        for a in f_args:
            if hasattr(a, 'META') or hasattr(a, 'headers') or hasattr(a, 'method'):
                request = a
                break
        if request is None:
            # fallback: assume first arg is the request
            request = f_args[0] if f_args else None

        # Prefer request.headers but fallback to common alternatives
        auth_header = ''
        try:
            auth_header = request.headers.get('Authorization', '')
        except Exception:
            auth_header = ''
        # Some servers put the header in META as HTTP_AUTHORIZATION
        if not auth_header and hasattr(request, 'META'):
            auth_header = request.META.get('HTTP_AUTHORIZATION', '') or request.META.get('Authorization', '')
        # Also allow token passed as GET/POST param for quick testing
        if not auth_header:
            try:
                if getattr(request, 'data', None):
                    auth_header = request.data.get('access_token', '')
                else:
                    auth_header = request.POST.get('access_token', '') if hasattr(request, 'POST') else ''
            except Exception:
                auth_header = ''
        # If token was provided as raw token (not "Bearer ..."), normalize
        if auth_header and not auth_header.startswith('Bearer '):
            auth_header = f'Bearer {auth_header}'
        if not auth_header or not auth_header.startswith('Bearer '):
            return error_response('auth_header_missing', 'Authorization header missing or invalid', http_status=status.HTTP_401_UNAUTHORIZED)
        token = auth_header.split(' ', 1)[1]
        if is_token_blacklisted(token):
            return error_response('token_revoked', 'Token has been revoked', http_status=status.HTTP_401_UNAUTHORIZED)
        try:
            payload = decode_token(token)
        except Exception:
            return error_response('invalid_token', 'Token inválido o expirado', http_status=status.HTTP_401_UNAUTHORIZED)
        # Attach payload to request object for downstream use
        try:
            request.jwt_payload = payload
        except Exception:
            pass

        # Call the original view function with the original args
        return view_func(*f_args, **kwargs)
    return _wrapped


def get_user_from_payload(payload: dict):
    """Return AuthUsuario instance from token payload 'sub' or None."""
    try:
        from .models import AuthUsuario
        sub = payload.get('sub')
        if not sub:
            return None
        return AuthUsuario.objects.filter(id=sub).first()
    except Exception:
        return None


def has_role(payload: dict, roles: list[str]) -> bool:
    if not payload:
        return False
    role = payload.get('role')
    return role in roles


def role_required(roles):
    """Decorator to require a role (works on views expecting JWT in Authorization header)."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            # First ensure valid JWT
            resp = jwt_required(lambda r: None)(request)
            if isinstance(resp, Response):
                return resp
            payload = getattr(request, 'jwt_payload', None)
            if not has_role(payload, roles):
                return error_response('forbidden', 'No tienes permisos para realizar esta acción', http_status=status.HTTP_403_FORBIDDEN)
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
