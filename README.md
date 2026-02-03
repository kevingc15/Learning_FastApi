# FastAPI User and Product Management API - Proyecto de Práctica

Este es un proyecto de práctica para aprender FastAPI. Una API REST construida con FastAPI para gestionar usuarios y productos, con soporte para autenticación básica y JWT (JSON Web Tokens). No está destinado para producción; es solo para fines educativos y experimentación.

## Características

- **Gestión de usuarios**: CRUD básico para usuarios (listar, obtener por ID).
- **Gestión de productos**: Endpoint simple para listar productos.
- **Autenticación básica**: Login con OAuth2 y tokens Bearer (en `basic_auth_users.py`).
- **Autenticación JWT**: Login seguro con tokens JWT expirables (en `auth_jwt.py`).
- **Documentación automática**: Accede a `/docs` (Swagger UI) o `/redoc` para explorar la API.
- **Validación con Pydantic**: Modelos robustos para datos de entrada/salida.

## Estructura del Proyecto

```
Fast_Api/
├── main.py                 # Punto de entrada principal (incluye routers)
├── routers/
│   ├── users.py            # Endpoints para usuarios (sin auth)
│   ├── products.py         # Endpoints para productos
│   ├── basic_auth_users.py # Autenticación básica con OAuth2
│   └── auth_jwt.py         # Autenticación con JWT
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo
```

## Instalación

1. **Clona o descarga el repositorio**.
2. **Crea un entorno virtual** (opcional pero recomendado):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # En Windows
   ```
3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. **Ejecuta el servidor**:

   ```bash
   uvicorn main:app --reload
   ```

   - La app estará disponible en `http://localhost:8000`.
   - `--reload` recarga automáticamente al editar código.

2. **Accede a la documentación**:
   - `http://localhost:8000/docs`: Interfaz interactiva (Swagger UI).
   - `http://localhost:8000/redoc`: Vista estática (ReDoc).

3. **Ejemplos de uso**:
   - **Listar usuarios**: `GET /users/`
   - **Obtener usuario por ID**: `GET /users/{id}`
   - **Login básico**: `POST /login` (en `basic_auth_users.py`, con form-data: username/password)
   - **Login JWT**: `POST /login` (en `auth_jwt.py`, con form-data: username/password)
   - **Perfil de usuario (JWT)**: `GET /users/me` (requiere token Bearer)

## Endpoints Principales

### Usuarios (sin autenticación)

- `GET /users/`: Lista todos los usuarios.
- `GET /users/{id}`: Obtiene un usuario por ID.

### Productos

- `GET /products/`: Lista productos (mensaje simple).

### Autenticación Básica (`basic_auth_users.py`)

- `POST /login`: Autentica y devuelve token Bearer.
- `GET /users/me`: Devuelve perfil del usuario autenticado (requiere token).

### Autenticación JWT (`auth_jwt.py`)

- `POST /login`: Autentica y devuelve token JWT (expira en 1 minuto por defecto).
- `GET /users/me`: Devuelve perfil del usuario autenticado (requiere token JWT).

**Notas de autenticación**:

- Usa herramientas como Postman o curl para probar.
- Tokens JWT son temporales; ajusta `ACCESS_TOKEN_EXPIRE_MINUTES` si necesitas más tiempo.
- Contraseñas están hasheadas con `pwdlib` (ejemplos en `users_db`).

## Configuración

- **SECRET_KEY**: Cambia la clave secreta en `auth_jwt.py` para producción (usa variables de entorno).
- **Base de datos**: Actualmente usa un diccionario en memoria (`users_db`). Integra con una BD real (e.g., SQLAlchemy) para persistencia.
- **CORS/Static Files**: Descomentado en `main.py` si necesitas servir archivos estáticos o permitir CORS.

## Troubleshooting

- **Error "Module not found"**: Asegúrate de activar el entorno virtual e instalar dependencias.
- **Errores de autenticación**: Verifica que el token sea válido y no expirado. Usa `/docs` para probar requests.
- **Puerto ocupado**: Cambia el puerto con `uvicorn main:app --port 8001`.
- **Problemas con JWT**: Instala `cryptography` si hay errores de decodificación: `pip install pyjwt[cryptography]`.
- **Python versión**: Requiere Python 3.8+. Verifica con `python --version`.

## Contribución

Este es un proyecto de práctica, pero si quieres contribuir:

1. Forkea el repo.
2. Crea una rama para tu feature.
3. Haz commits descriptivos.
4. Abre un Pull Request.

## Licencia

Este proyecto es de código abierto y para aprendizaje. Úsalo libremente, pero no para producción sin modificaciones.

---

**Nota**: Este proyecto es solo para práctica y aprendizaje de FastAPI. No implementa seguridad completa ni escalabilidad para entornos reales.

**Autor**: Kevin.  
**Fecha**: Febrero 2026.  
Si tienes preguntas, abre un issue en Git.
