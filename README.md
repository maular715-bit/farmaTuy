# FarmaTuy 

Breve README con pasos para poner en marcha el proyecto.

Requisitos
- Python 3.10+ (se probó con 3.12)
- Git (opcional)

Configuración rápida (recomendado: virtualenv)

1) Crear y activar entorno virtual

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Windows cmd
.venv\Scripts\activate.bat
# mac / linux
source .venv/bin/activate
```

2) Instalar dependencias

```bash
pip install -r requerimientos.txt
```

3) Variables de entorno (opcional)
- `DJANGO_SECRET_KEY` — si desea reemplazar la clave por defecto en `farmatuy_project/settings.py`.
- `JWT_SECRET` — secreto para firmar JWT (si no se define, usa `change-me`).
- `JWT_ALGORITHM` — algoritmo JWT (por defecto `HS256`).

4) Migraciones y superusuario

```bash
python manage.py makemigrations
python manage.py migrate
# Crear superusuario (ya creado en este entorno en ejemplos):
python manage.py createsuperuser
```

Nota: en este repo se creó un superusuario de ejemplo durante la migración: `admin_farmatuy` (contraseña `PruebaAdmin`). Puedes cambiarla o eliminarla en el admin.

5) Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

API y endpoints principales

- Root API: `/api/`
- Farmacias: `/api/farmacias/` (CRUD)
- Medicamentos: `/api/medicamentos/` (CRUD)
- Inventario: `/api/inventario/` (CRUD)
- Tipos: `/api/tipos/` (CRUD)
- Usuarios: `/api/usuarios/` (CRUD)

Autenticación (JWT)

- Registro: `POST /api/auth/register/`  JSON: `{ "username": "u", "email": "e@x", "password": "p" }`
- Login: `POST /api/auth/login/` JSON: `{ "email": "e@x", "password": "p" }` → devuelve `access_token` (Bearer JWT).
- Obtener perfil: `GET /api/auth/me/` con cabecera `Authorization: Bearer <token>`.
- Logout (revocar token): `POST /api/auth/logout/` con cabecera `Authorization: Bearer <token>` — el token queda en la blacklist.

Social login

Se expone `POST /api/auth/social/` con body `{ "provider": "google" | "github", "token": "<id_or_access_token>" }`.
- `google`: valida `id_token` contra `https://oauth2.googleapis.com/tokeninfo`.
- `github`: valida `access_token` contra `https://api.github.com/user`.

Al autenticarse vía social, el servidor crea (si no existe) un `AuthUsuario` + `Usuario` local y devuelve un JWT.


**Formato de errores**

Las respuestas de error usan un formato uniforme JSON con un código y mensaje. Ejemplos:

- Error de credenciales inválidas (login):

```json
{
	"error": {
		"code": "invalid_credentials",
		"message": "Credenciales inválidas"
	}
}
```

- Error cabecera Authorization faltante:

```json
{
	"error": {
		"code": "auth_header_missing",
		"message": "Authorization header missing or invalid"
	}
}
```

- Error token revocado o inválido:

```json
{
	"error": {
		"code": "token_revoked",
		"message": "Token has been revoked"
	}
}
```

Protección de endpoints

Las operaciones que modifican datos (crear, actualizar, eliminar) están protegidas con JWT. Para llamar a estas rutas, añade la cabecera:

```
Authorization: Bearer <access_token>
```

Ejemplos `curl`

- Login (obtener token):

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
	-H "Content-Type: application/json" \
	-d '{"email":"admin@example.com","password":"PruebaAdmin"}'
```

- Crear farmacia (protegido):

```bash
curl -X POST http://127.0.0.1:8000/api/farmacias/ \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer <access_token>" \
	-d '{"razon_social":"Farmacia X","rif":"J-12345678-9","estado":"Estado","municipio":"Municipio","parroquia":"Parroquia"}'
```

- Logout (revocar token):

```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
	-H "Authorization: Bearer <access_token>"
```

