# API Contract — Eco-Red Backend

> Documento de integración para el equipo **frontend**. Define cómo conectar la
> aplicación con el microservicio Django REST, cómo autenticarse y el formato
> exacto de cada endpoint.

---

## 1. Información general

| Dato | Valor |
|---|---|
| **URL base (desarrollo)** | `http://127.0.0.1:8000/api` |
| **Formato de datos** | `application/json` |
| **Autenticación** | Firebase Authentication (ID token en header `Authorization`) |
| **Documentación interactiva (Swagger)** | `http://127.0.0.1:8000/api/docs/` |
| **Esquema OpenAPI** | `http://127.0.0.1:8000/api/schema/` |

En el frontend React la URL base se define en `VITE_API_URL` (`.env`). Si el
proyecto se publica tras un **API Gateway (NGINX)**, solo cambia esa variable;
ningún otro código debe depender de la URL.

> **CORS:** el backend solo acepta peticiones desde los orígenes listados en
> `CORS_ALLOWED_ORIGINS` (por defecto `http://localhost:5173`). Si el frontend
> corre en otro puerto o dominio, el equipo de backend debe agregarlo.

---

## 2. Autenticación (paso previo obligatorio)

La autenticación se realiza **en el cliente con el SDK de Firebase**. El backend
**no** recibe contraseñas: recibe el **ID token** de Firebase en cada petición.

```js
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";

const auth = getAuth();
await signInWithEmailAndPassword(auth, email, password);

// Obtener el ID token vigente (Firebase lo renueva automáticamente):
const idToken = await auth.currentUser.getIdToken();
```

Toda petición a la API (excepto `/health/` y las de documentación) debe incluir:

```
Authorization: Bearer <idToken>
Content-Type: application/json
```

> La aplicación de referencia en este repositorio ya centraliza esto en
> `frontend/src/shared/services/httpClient.js` (interceptor de Axios que
> adjunta el token automáticamente).

---

## 3. Roles y perfiles

Cada usuario Firebase registra un **perfil** con un rol en la colección `users`:

| Rol | Valor en API | Descripción |
|---|---|---|
| Usuario | `usuario` | Consumidor/ciudadano |
| Empresa | `empresa` | Publica materiales y experiencias |
| Admin | `admin` | Administración (se asigna manualmente, no se auto-registra) |

**Cómo saber el rol del usuario conectado:**

```
GET /api/auth/me/
Authorization: Bearer <idToken>
```

```json
{
  "id": "66d3f2a1b8c9d0e1f2a3b4c6",
  "uid": "abc123firebaseuid",
  "email": "usuario@correo.com",
  "nombre": "Empresa ABC",
  "role": "empresa",
  "created_at": "2026-08-12T10:00:00+00:00"
}
```

Usa `role` para decidir qué secciones de la interfaz mostrar (ej. el módulo de
administración solo si `role === "admin"`).

---

## 4. Registro de usuario (flujo en 2 pasos)

El registro público solo permite los roles `usuario` y `empresa`.

**Paso 1 — Crear la cuenta en Firebase (cliente):**

```js
import { createUserWithEmailAndPassword } from "firebase/auth";
await createUserWithEmailAndPassword(auth, email, password);
```

**Paso 2 — Registrar el perfil en el backend:**

```
POST /api/auth/register/
Authorization: Bearer <idToken>
Content-Type: application/json
```

```json
{
  "nombre": "Empresa ABC",
  "role": "empresa"
}
```

**Respuesta 201 Created:**

```json
{
  "id": "66d3f2a1b8c9d0e1f2a3b4c6",
  "uid": "abc123firebaseuid",
  "email": "usuario@correo.com",
  "nombre": "Empresa ABC",
  "role": "empresa",
  "created_at": "2026-08-12T10:00:00+00:00"
}
```

> El `uid` se toma del token, **nunca** del cuerpo de la petición.

---

## 5. Endpoints

### 5.1 Salud

| Método | Ruta | Autenticación |
|---|---|---|
| GET | `/health/` | No |

```
GET /health/  →  200
```

```json
{ "status": "ok" }
```

### 5.2 Registro y perfil

| Método | Ruta | Autenticación |
|---|---|---|
| POST | `/auth/register/` | Bearer token |
| GET | `/auth/me/` | Bearer token |

**Errores posibles de `POST /auth/register/`:**

| Código | Significado |
|---|---|
| `400` | Validación (rol no permitido, nombre vacío/corto) |
| `401` | Token ausente o inválido |
| `409` | El perfil ya existe para ese uid |

**`GET /auth/me/`:** `200` perfil, `401` sin token, `404` si el perfil aún no se ha registrado.

### 5.3 Administración de usuarios (solo `admin`)

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/users/` | Lista todos los perfiles |
| GET | `/users/{uid}/` | Obtiene un perfil por UID de Firebase |
| PATCH | `/users/{uid}/role/` | Cambia el rol de un perfil |

**PATCH `/users/{uid}/role/`** — cuerpo:

```json
{ "role": "admin" }
```

**Errores:** `400` rol inválido, `401` sin token, `403` no es admin, `404` uid inexistente.

### 5.4 Empresas

| Método | Ruta | Autenticación |
|---|---|---|
| GET | `/companies/` | Bearer token |
| POST | `/companies/` | Bearer token |

**GET `/companies/`** → `200` lista de las empresas del usuario conectado:

```json
[
  {
    "id": "66d3f2a1b8c9d0e1f2a3b4c5",
    "owner_uid": "abc123firebaseuid",
    "name": "EcoRed Demo",
    "nit": "900000001",
    "city": "Bogotá",
    "sector": "Manufactura",
    "size": "Mediana",
    "employes": "25",
    "created_at": "2026-08-12T10:00:00+00:00"
  }
]
```

**POST `/companies/`** — cuerpo:

```json
{
  "name": "Empresa ABC",
  "nit": "900123456-7",
  "city": "Bogotá",
  "sector": "Reciclaje",
  "size": "Mediana",
  "employes": "25"
}
```

**Respuesta `201 Created`:**

```json
{ "id": "66d3f2a1b8c9d0e1f2a3b4c5" }
```

### 5.5 Materiales

| Método | Ruta | Autenticación |
|---|---|---|
| GET | `/materials/` | Bearer token |
| POST | `/materials/` | Bearer token |

Devuelven las publicaciones de las empresas del usuario conectado.

**GET `/materials/`** → `200` lista. Cada elemento:

```json
{
  "id": "66d3f2a1b8c9d0e1f2a3b4c7",
  "company_id": "66d3f2a1b8c9d0e1f2a3b4c5",
  "material_type": "Cartón",
  "quantity": 80,
  "unit": "kg",
  "location": "Bogotá",
  "price": 15000,
  "material-status": "disponible",
  "status": "available",
  "published_by": "abc123firebaseuid",
  "created_at": "2026-08-12T10:05:00+00:00"
}
```

> ⚠️ Nota: el campo `status_Material` enviado al crear se devuelve como
> `material-status` (con guion). Conocido y documentado para el frontend.

**POST `/materials/`** — cuerpo (`company_id` es el `id` devuelto al crear la empresa):

```json
{
  "company_id": "66d3f2a1b8c9d0e1f2a3b4c5",
  "material_type": "Cartón",
  "quantity": 80,
  "unit": "kg",
  "location": "Bogotá",
  "price": 15000,
  "status_Material": "disponible",
  "status": "available"
}
```

**Respuesta `201 Created`:**

```json
{ "id": "66d3f2a1b8c9d0e1f2a3b4c7" }
```

---

## 6. Códigos de error comunes

| Código | Significado | Acción sugerida en frontend |
|---|---|---|
| `400` | Datos inválidos. Cuerpo: `{"campo": ["mensaje"]}` | Mostrar el mensaje del campo |
| `401` | Token ausente/inválido/vencido | Cerrar sesión y redirigir a login |
| `403` | Autenticado pero sin permiso (rol insuficiente) | Ocultar/deshabilitar la acción |
| `404` | Recurso no existe (perfil no registrado, uid inexistente) | Mostrar "no encontrado" |
| `409` | Conflicto (perfil ya registrado) | Redirigir al dashboard o actualizar perfil |

Errores de autenticación: `{"detail": "..."}`. Errores de validación de DRF:
`{"nombre": ["Asegúrese de que este campo tenga al menos 2 caracteres."]}`.

---

## 7. Ejemplo completo (fetch)

```js
const API_URL = import.meta.env.VITE_API_URL; // http://127.0.0.1:8000/api

async function registerProfile({ nombre, role }) {
  const idToken = await auth.currentUser.getIdToken();

  const response = await fetch(`${API_URL}/auth/register/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${idToken}`,
    },
    body: JSON.stringify({ nombre, role }),
  });

  if (!response.ok) {
    const data = await response.json();
    throw new Error(JSON.stringify(data));
  }

  return response.json();
}
```

---

## 8. Notas para el equipo frontend

1. **No almacenen el ID token en `localStorage`.** Firebase lo gestiona y lo
   renueva; usen `getIdToken()` al momento de cada petición (o un interceptor).
2. **El usuario puede no tener perfil todavía** (recién se creó en Firebase).
   `GET /auth/me/` devolverá `404`; es el momento de mostrar el formulario de
   registro de perfil (nombre + rol).
3. **El rol decide la UI:** `usuario` (ver), `empresa` (publicar), `admin`
   (gestionar usuarios).
4. **Para probar sin implementar todo**, usen Swagger en
   `http://127.0.0.1:8000/api/docs/` con el botón **Authorize** pegando el ID token.
5. Cualquier cambio de contrato (nuevos campos, códigos, rutas) se refleja
   automáticamente en el esquema OpenAPI de `/api/schema/`.
