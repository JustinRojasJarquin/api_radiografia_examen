# API Radiografías

API backend para la gestión de placas radiográficas de pacientes. Permite autenticación con Google SSO, subida de imágenes a Cloudinary y CRUD completo de registros radiográficos.

## Instalación

```bash
git clone https://github.com/JustinRojasJarquin/api_radiografia_examen
cd api_radiografia_examen
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Crear el archivo `.env` en la raíz del proyecto:

```env
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
GOOGLE_CLIENT_ID=tu_google_client_id
SIGNED_URL_SECRET=clave_secreta_para_firmar_urls
SIGNED_URL_EXPIRE_MINUTES=5
```

Crear la base de datos y correr el proyecto:

```bash
python manage.py migrate
python manage.py runserver
```

La documentación Swagger estará disponible en: `http://localhost:8000/swagger/`

## Endpoints

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | `/api/v1/auth/google/login` | Login con Google, retorna JWT | No |
| GET | `/api/v1/records/` | Listar registros (paginación y filtros) | JWT |
| POST | `/api/v1/records/` | Crear registro con imagen (multipart) | JWT |
| GET | `/api/v1/records/{id}/` | Detalle de un registro | JWT |
| PUT | `/api/v1/records/{id}/` | Actualizar registro | JWT |
| DELETE | `/api/v1/records/{id}/` | Eliminar registro | JWT |
| GET | `/api/v1/records/{id}/signed-image-url/` | Obtener URL firmada de imagen (expira en 5 min) | JWT |
| GET | `/api/v1/images/view/?token=...` | Ver imagen usando URL firmada | No |

## Filtros disponibles en GET /records

- `?page=1&page_size=20` — paginación
- `?patient_full_name=Juan` — filtrar por nombre
- `?patient_identifier=123` — filtrar por identificación
- `?study_date=2024-01-15` — filtrar por fecha
- `?search=texto` — búsqueda general
- `?order_by=study_date` o `?order_by=-study_date` — ordenamiento

## Arquitectura

El proyecto está organizado en capas:

- **routes** — vistas Django que reciben las peticiones HTTP
- **services** — lógica de negocio
- **repositories** — acceso a base de datos con SQLAlchemy
- **schemas** — validación de datos con Pydantic

## Decisiones técnicas

- **Django** como framework principal para el manejo de requests y configuración.
- **SQLAlchemy + Alembic** para el ORM y migraciones, en lugar del ORM de Django, para mayor flexibilidad y control sobre las queries.
- **SQLite** como base de datos por simplicidad en desarrollo.
- **Cloudinary** para almacenamiento de imágenes con CDN, devolviendo una URL pública por registro.
- **Google OAuth2** para autenticación SSO sin manejar contraseñas.
- **JWT** para sesiones stateless en endpoints protegidos.
- **Pydantic** para validación estricta de entrada y salida de datos.
