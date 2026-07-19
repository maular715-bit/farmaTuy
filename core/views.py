from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Farmacia, Medicamento, InventarioFarmacia, Tipo, Usuario, AuthUsuario
from .serializers import (
    FarmaciaSerializer,
    MedicamentoSerializer,
    InventarioSerializer,
    TipoSerializer,
    UsuarioSerializer,
    AuthUsuarioSerializer,
    RegisterSerializer,
    LoginSerializer,
    UserPublicSerializer,
)
from .auth_utils import hash_password, verify_password, create_token, decode_token
from .auth_utils import jwt_required, blacklist_token, get_user_from_payload, error_response
import requests
from database.db import get_db
from controllers.medicamento_controller import get_medicamentos
from models.medicamento import Medicamento as SAMedicamento
from sqlalchemy import select, func, and_, or_
import math


class SoftDeleteModelViewSet(viewsets.ModelViewSet):
    """ModelViewSet base that filters estatus=True and soft-deletes on destroy."""
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(estatus=True)

    def perform_create(self, serializer):
        serializer.save(estatus=True)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estatus = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class FarmaciaViewSet(SoftDeleteModelViewSet):
    queryset = Farmacia.objects.all()
    serializer_class = FarmaciaSerializer

    # allow responsable and supervisor to create/update/delete
    from .auth_utils import role_required

    @role_required(["farmacia_responsable", "supervisor"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @role_required(["farmacia_responsable", "supervisor"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @role_required(["farmacia_responsable", "supervisor"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class MedicamentoViewSet(SoftDeleteModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer

    from .auth_utils import role_required

    @role_required(["farmacia_responsable", "supervisor"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @role_required(["farmacia_responsable", "supervisor"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @role_required(["farmacia_responsable", "supervisor"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class InventarioViewSet(SoftDeleteModelViewSet):
    queryset = InventarioFarmacia.objects.all()
    serializer_class = InventarioSerializer

    from .auth_utils import role_required

    @role_required(["farmacia_responsable", "supervisor"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @role_required(["farmacia_responsable", "supervisor"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @role_required(["farmacia_responsable", "supervisor"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class TipoViewSet(viewsets.ModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer

    from .auth_utils import role_required

    @role_required(["supervisor"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @role_required(["supervisor"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @role_required(["supervisor"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    from .auth_utils import role_required

    @role_required(["supervisor"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @role_required(["supervisor"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @role_required(["supervisor"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        email = data['email'].strip().lower()
        username = data['username'].strip()
        password = data['password']

        if AuthUsuario.objects.filter(correo=email).exists() or Usuario.objects.filter(username=username).exists():
            return error_response('user_exists', 'Ya existe un usuario con ese correo o nombre de usuario', http_status=status.HTTP_400_BAD_REQUEST)

        hashed = hash_password(password)
        auth_user = AuthUsuario.objects.create(
            correo=email,
            password_hash=hashed,
            nombre_primero=data.get('nombre_primero', ''),
            apellido_paterno=data.get('apellido_paterno', ''),
        )

        usuario = Usuario.objects.create(auth_usuario=auth_user, username=username)

        return Response({"id": str(usuario.id), "username": usuario.username, "email": auth_user.correo}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        email = data['email'].strip().lower()
        password = data['password']

        try:
            auth_user = AuthUsuario.objects.get(correo=email)
        except AuthUsuario.DoesNotExist:
            return error_response('invalid_credentials', 'Credenciales inválidas', http_status=status.HTTP_401_UNAUTHORIZED)

        if not verify_password(password, auth_user.password_hash):
            return error_response('invalid_credentials', 'Credenciales inválidas', http_status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = Usuario.objects.get(auth_usuario=auth_user)
        except Usuario.DoesNotExist:
            return error_response('profile_missing', 'Perfil de usuario no encontrado', http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        payload = {"sub": str(auth_user.id), "username": user.username, "email": auth_user.correo}
        try:
            payload['role'] = user.role
        except Exception:
            payload['role'] = 'farmacia_responsable'
        token = create_token(payload)

        return Response({"access_token": token, "token_type": "Bearer"})


class MeView(APIView):
    def get(self, request):
        # Use decorator or manual token processing
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return error_response('auth_header_missing', 'Authorization header missing or invalid', http_status=status.HTTP_401_UNAUTHORIZED)
        token = auth_header.split(' ', 1)[1]
        if jwt_required(lambda r: None)(request) is not None:
            # jwt_required returns a Response on error; if ok it returns the view's return (None here)
            pass
        try:
            payload = decode_token(token)
        except Exception:
            return error_response('invalid_token', 'Token inválido', http_status=status.HTTP_401_UNAUTHORIZED)

        user = get_user_from_payload(payload)
        return Response({"user": {"id": str(payload.get('sub')), "username": payload.get('username'), "email": payload.get('email')}})


class LogoutView(APIView):
    def post(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return error_response('auth_header_missing', 'Authorization header missing or invalid', http_status=status.HTTP_401_UNAUTHORIZED)
        token = auth_header.split(' ', 1)[1]
        blacklist_token(token)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SocialAuthView(APIView):
    """Social login endpoint. Accepts provider and token.

    POST body example:
    {"provider":"google", "token":"<id_token>"}
    or
    {"provider":"github", "token":"<access_token>"}
    """
    def post(self, request):
        data = request.data
        provider = (data.get('provider') or '').lower()
        token = data.get('token')
        if not provider or not token:
            return error_response('invalid_request', 'provider and token are required', http_status=status.HTTP_400_BAD_REQUEST)

        user_info = None
        try:
            if provider == 'google':
                # Verify Google ID token via Google's tokeninfo endpoint
                resp = requests.get('https://oauth2.googleapis.com/tokeninfo', params={'id_token': token}, timeout=5)
                if resp.status_code != 200:
                    return error_response('provider_token_invalid', 'Token de Google inválido', http_status=status.HTTP_401_UNAUTHORIZED)
                user_info = resp.json()
                provider_id = user_info.get('sub')
                email = user_info.get('email')
                name = user_info.get('name') or ''
            elif provider == 'github':
                # Use GitHub API to get user info
                headers = {'Authorization': f'token {token}'}
                resp = requests.get('https://api.github.com/user', headers=headers, timeout=5)
                if resp.status_code != 200:
                    return error_response('provider_token_invalid', 'Token de GitHub inválido', http_status=status.HTTP_401_UNAUTHORIZED)
                user_info = resp.json()
                provider_id = str(user_info.get('id'))
                email = user_info.get('email') or ''
                name = user_info.get('name') or user_info.get('login')
            else:
                return error_response('unsupported_provider', 'Proveedor no soportado', http_status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException:
            return error_response('provider_unavailable', 'Error verificando token con el proveedor', http_status=status.HTTP_502_BAD_GATEWAY)

        # Create or get local user (AuthUsuario + Usuario)
        try:
            auth_user = AuthUsuario.objects.filter(correo=email).first() if email else None
            if not auth_user:
                # Create an AuthUsuario with a random password hash (user won't use it)
                hashed = hash_password(''.join(['s', provider, provider_id]))
                auth_user = AuthUsuario.objects.create(correo=email or f'{provider}_{provider_id}@noemail', password_hash=hashed, nombre_primero=name)
            usuario = Usuario.objects.filter(auth_usuario=auth_user).first()
            if not usuario:
                # generate a username
                base_username = (email.split('@')[0] if email else f'{provider}_{provider_id}')
                username = base_username
                suffix = 1
                while Usuario.objects.filter(username=username).exists():
                    username = f"{base_username}{suffix}"
                    suffix += 1
                usuario = Usuario.objects.create(auth_usuario=auth_user, username=username)

            payload = {"sub": str(auth_user.id), "username": usuario.username, "email": auth_user.correo}
            # include role in token
            try:
                payload['role'] = usuario.role
            except Exception:
                payload['role'] = 'farmacia_responsable'
            jwt = create_token(payload)
            return Response({"access_token": jwt, "token_type": "Bearer"})
        except Exception as e:
            return error_response('internal_error', 'Error interno creando usuario', http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    class MedicamentosAPI(APIView):
        """Endpoint simple que delega en controllers/medicamento_controller.get_medicamentos

        Parámetros query: `q` (opcional), `skip`, `limit`
        """
        def get(self, request):
            # Parámetros de filtro y paginación
            q = request.query_params.get('q')
            try:
                page = max(1, int(request.query_params.get('page', 1)))
            except Exception:
                page = 1
            try:
                page_size = int(request.query_params.get('page_size', 10))
            except Exception:
                page_size = 10

            # filtros adicionales (ids de relaciones o disposicion)
            principio_id = request.query_params.get('principio_id')
            presentacion_id = request.query_params.get('presentacion_id')
            disposicion = request.query_params.get('disposicion')

            offset = (page - 1) * page_size

            with get_db() as db:
                # Construir condiciones
                conditions = [SAMedicamento.estatus == True]
                if q:
                    like_q = f"%{q}%"
                    conditions.append(or_(SAMedicamento.medicamento.ilike(like_q), SAMedicamento.descripcion.ilike(like_q)))
                if principio_id:
                    try:
                        conditions.append(SAMedicamento.tipo_principio_activo_id == int(principio_id))
                    except Exception:
                        pass
                if presentacion_id:
                    try:
                        conditions.append(SAMedicamento.tipo_presentacion_id == int(presentacion_id))
                    except Exception:
                        pass
                if disposicion:
                    conditions.append(SAMedicamento.disposicion == disposicion)

                where_clause = and_(*conditions)

                total = db.scalar(select(func.count()).select_from(SAMedicamento).where(where_clause)) or 0

                stmt = select(SAMedicamento).where(where_clause).offset(offset).limit(page_size)
                meds = list(db.scalars(stmt))

                data = [
                    {
                        "id": m.id,
                        "medicamento": m.medicamento,
                        "descripcion": m.descripcion,
                        "disposicion": m.disposicion,
                    }
                    for m in meds
                ]

            total_pages = math.ceil(total / page_size) if page_size else 1
            return Response({"results": data, "page": page, "page_size": page_size, "total": total, "total_pages": total_pages})

