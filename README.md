# Eco-Red — Microservicio de Autenticación y Gestión de Materiales

Proyecto en desarrollo de un **microservicio de autenticación** para una plataforma de economía circular (gestión de empresas y publicaciones de materiales reciclables).

La autenticación se delega a **Firebase Authentication** (correo/contraseña y Google), el backend expone una **API REST con Django REST Framework** (protegida con tokens Firebase), los datos se almacenan en **MongoDB Atlas**, y el **frontend React + Vite** consume esa API adjuntando un ID token vigente.

---

## 1. Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Python 3.13, Django 6.0, Django REST Framework 3.17 |
| Autenticación | Firebase Admin SDK (validación de ID tokens) + Firebase Authentication |
| Base de datos | MongoDB Atlas (PyMongo) |
| Frontend | React 19, Vite 8, React Router 7, Axios, Bootstrap 5 |
| Configuración | variables de entorno (`.env`) |

---

## 2. Arquitectura general

```mermaid
flowchart LR
  FE[Frontend React :5173] -->|1. login Firebase| FB[Firebase Authentication]
  FB -->|2. ID token| FE
  FE -->|3. Authorization: Bearer token| API[Backend Django :8000]
  API -->|4. valida token| SDK[Firebase Admin SDK]
  API -->|5. CRUD| MONGO[(MongoDB Atlas)]
```

Flujo resumido:

1. El usuario inicia sesión desde el frontend; Firebase emite un ID token.
2. El usuario registra su perfil (`POST /api/auth/register/`) con un rol
   (`usuario`, `empresa` o `admin` asignado manualmente).
3. Cada petición HTTP del frontend adjunta `Authorization: Bearer <id_token>`.
4. El backend valida el token contra Firebase y expone el `uid` en `request.firebase_user`.
5. Las colecciones (`users`, `companies`, `material_listings`) se consultan/insertan en MongoDB filtrando por ese `uid` y, según el endpoint, verificando el rol del perfil.

---

## 3. Estructura del repositorio

```text
Eco-Red - NewProject/
├── backend/                  # Microservicio Django REST
│   ├── config/               # settings, urls, wsgi/asgi
│   ├── companies/            # App de empresas y materiales
│   │   ├── firebase_auth.py  # Autenticación Firebase (DRF)
│   │   ├── mongo.py          # Conexión a MongoDB Atlas (companies, materials, users)
│   │   ├── views.py          # ViewSets: companies y materials
│   │   ├── urls.py           # Rutas /api/*
│   │   └── management/commands/seed_demo.py  # Datos de ejemplo
│   ├── users/                # App de perfiles y roles (registro)
│   │   ├── repositories/     # Acceso a MongoDB (users)
│   │   ├── services/         # Lógica de negocio (registro, roles)
│   │   ├── permissions.py    # IsAdminUser (rol admin)
│   │   ├── serializers.py    # Validación de entrada/salida
│   │   ├── views.py          # register, me, administración de perfiles
│   │   ├── urls.py           # Rutas /api/auth/* y /api/users/*
│   │   └── management/commands/seed_admin.py  # Asigna rol admin
│   ├── firebase-service-account.json  # Credencial de servicio Firebase (no versionar)
│   ├── .env                  # Variables de entorno (no versionar)
│   ├── firebase-materials-simple.http  # Pruebas con extensión REST Client
│   └── requirements.txt
├── frontend/                 # Cliente React + Vite
│   ├── .env.example          # Plantilla de variables VITE_*
│   └── src/
│       ├── config/           # env.js y firebase.js
│       ├── features/         # auth, companies, home, materials
│       └── shared/           # httpClient, componentes y utilidades comunes
└── README.md
```

---

## 4. Requisitos previos

- **Python 3.12+** (verificado con 3.13)
- **Node.js 18+** (con `npm`)
- Cuenta de **Firebase** con un proyecto (Authentication habilitado y una **aplicación web** registrada)
- Cuenta de **MongoDB Atlas** con un cluster
- (Opcional) Extensión **REST Client** en VS Code para probar el `.http`

---

## 5. Puesta en marcha — Backend

Todos los comandos se ejecutan dentro de la carpeta `backend/`.

### 5.1 Crear entorno virtual e instalar dependencias

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS
pip install -r requirements.txt
```

### 5.2 Configuración (`.env` y credencial Firebase)

El archivo `backend/.env` ya existe en este equipo y contiene:

```env
DJANGO_SECRET_KEY='django-insecure-...'
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
APP_ENV=dev
PORT=8000

MONGODB_URI='mongodb+srv://...'
MONGODB_DB_NAME=ecored_circular_db

CORS_ALLOWED_ORIGINS=http://localhost:5173
FIREBASE_CREDENTIALS_PATH=./firebase-service-account.json
```

Además debe existir el archivo `backend/firebase-service-account.json` (la credencial de servicio descargada desde **Firebase Console → Configuración del proyecto → Cuentas de servicio → Generar nueva clave privada**). Este archivo ya está presente localmente.

> ⚠️ Ambos archivos contienen secretos. No deben subirse al repositorio (ver [sección de seguridad](#9-hallazgos-código-faltante-y-riesgos)).

### 5.3 Migraciones (para el panel de administración)

```bash
python manage.py migrate
```

### 5.4 (Opcional) Datos de ejemplo

```bash
python manage.py seed_demo
```

> ⚠️ **Pendiente:** este comando requiere los archivos vacíos
> `backend/companies/management/__init__.py` y
> `backend/companies/management/commands/__init__.py`, que **no existen** en el
> repositorio. Sin ellos Django lanza `Unknown command: 'seed_demo'`. Ver
> [hallazgo #1](#hallazgos-código-faltante-y-riesgos).

### 5.5 Ejecutar el servidor

```bash
python manage.py runserver
```

El backend queda disponible en **http://127.0.0.1:8000**.

---

## 6. Puesta en marcha — Frontend

Todos los comandos se ejecutan dentro de la carpeta `frontend/`.

### 6.1 Crear el archivo `.env`

> ⚠️ **Pendiente:** el archivo `frontend/.env` **no existe** en el proyecto. Sin
> él, el frontend no arranca y muestra la pantalla de diagnóstico "Configuración
> incompleta". Ver [hallazgo #2](#hallazgos-código-faltante-y-riesgos).

Copie la plantilla y complétela:

```bash
cd frontend
Copy-Item .env.example .env    # Windows PowerShell
# cp .env.example .env         # Linux / macOS
```

Contenido resultante:

```env
# URL base del backend. No debe terminar en barra.
VITE_API_URL=http://localhost:8000/api

# Configuración pública de la aplicación web registrada en Firebase.
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_PROJECT_ID=
VITE_FIREBASE_APP_ID=
```

Estos valores se obtienen en **Firebase Console → Configuración del proyecto →
Sus apps → aplicación web → Configuración del SDK**. Para este proyecto los
valores conocidos son:

| Variable | Valor |
|---|---|
| `VITE_API_URL` | `http://localhost:8000/api` |
| `VITE_FIREBASE_API_KEY` | `AIzaSyAvrtadjsZgY8sJd-wulMxvL8zcKr2fbbg` |
| `VITE_FIREBASE_PROJECT_ID` | `ecored-c8374` |
| `VITE_FIREBASE_AUTH_DOMAIN` | `ecored-c8374.firebaseapp.com` (o `ecored-c8374.web.app`) |
| `VITE_FIREBASE_APP_ID` | **obtener de Firebase Console** (formato `1:<número>:web:<hash>`) |

Después de modificar `.env`, reinicie Vite.

### 6.2 Instalar dependencias

```bash
npm install
```

### 6.3 Ejecutar el frontend

```bash
npm run dev
```

El frontend queda disponible en **http://localhost:5173**.

### 6.4 Validar calidad

```bash
npm run lint
npm run build
# o ambas
npm run check
```

---

## 7. URLs de prueba

### 7.1 Backend (Django REST, puerto 8000)

| Método | URL | Descripción | Autenticación |
|---|---|---|---|
| GET | `http://127.0.0.1:8000/api/health/` | Verifica que el backend responde → `{"status": "ok"}` | Pública |
| POST | `http://127.0.0.1:8000/api/auth/register/` | Registra el perfil (nombre + rol `usuario`/`empresa`) del usuario autenticado | Bearer token |
| GET | `http://127.0.0.1:8000/api/auth/me/` | Devuelve el perfil del usuario autenticado | Bearer token |
| GET | `http://127.0.0.1:8000/api/users/` | Lista todos los perfiles (**solo admin**) | Bearer token (admin) |
| GET | `http://127.0.0.1:8000/api/users/{uid}/` | Obtiene el perfil de un usuario (**solo admin**) | Bearer token (admin) |
| PATCH | `http://127.0.0.1:8000/api/users/{uid}/role/` | Cambia el rol de un perfil (**solo admin**) | Bearer token (admin) |
| GET | `http://127.0.0.1:8000/api/companies/` | Lista las empresas del usuario autenticado | Bearer token |
| POST | `http://127.0.0.1:8000/api/companies/` | Crea una empresa | Bearer token |
| GET | `http://127.0.0.1:8000/api/materials/` | Lista publicaciones de las empresas del usuario | Bearer token |
| POST | `http://127.0.0.1:8000/api/materials/` | Crea una publicación de material | Bearer token |
| — | `http://127.0.0.1:8000/admin/` | Panel de administración de Django | Usuario Django |
| GET | `http://127.0.0.1:8000/api/docs/` | **Swagger UI** (documentación interactiva) | — |
| GET | `http://127.0.0.1:8000/api/schema/` | Esquema OpenAPI en JSON (`?format=yaml` para YAML) | — |
| GET | `http://127.0.0.1:8000/api/redoc/` | ReDoc (documentación alternativa) | — |

Cuerpo de ejemplo para **POST /api/companies/**:

```json
{
  "name": "EcoRed Demo",
  "nit": "900123456-7",
  "city": "Bogotá",
  "sector": "Reciclaje",
  "size": "Mediana",
  "employes": "25"
}
```

Cuerpo de ejemplo para **POST /api/materials/** (`company_id` debe ser el `id`
devuelto al crear la empresa):

```json
{
  "company_id": "665a4f0e1a2b3c4d5e6f7080",
  "material_type": "Cartón",
  "quantity": 80,
  "unit": "kg",
  "location": "Bogotá",
  "price": 15000,
  "status_Material": "disponible",
  "status": "available"
}
```

> Las peticiones sin token o con token inválido responden **401 Unauthorized**.
> Un usuario autenticado sin rol `admin` recibe **403 Forbidden** en
> `/api/users/`.

### 7.2 Frontend (Vite, puerto 5173)

| URL | Descripción |
|---|---|
| `http://localhost:5173` | Redirige a `/login` o `/home` según la sesión |
| `http://localhost:5173/login` | Inicio de sesión (correo/contraseña o Google) |
| `http://localhost:5173/home` | Panel principal del usuario autenticado |
| `http://localhost:5173/companies` | Formulario para crear empresas (protegida) |
| `http://localhost:5173/materials` | Crear y listar publicaciones (protegida) |

---

## 8. Cómo probar el flujo completo

### Opción A — Desde el frontend (recomendado)

1. Cree un usuario de prueba en **Firebase Console → Authentication → Users →
   Add user** (o use el botón "Ingresar con Google").
2. Inicie backend y frontend (`runserver` + `npm run dev`).
3. Abra `http://localhost:5173`, inicie sesión.
4. Cree una empresa en `/companies`.
5. Copie el `id` de esa empresa (visible en la base de datos o mediante la API).
6. En `/materials` seleccione la empresa y publique un material.

### Opción B — API con REST Client (archivo `.http`)

1. Abra `backend/firebase-materials-simple.http` en VS Code con la extensión **REST Client**.
2. Edite `@EMAIL` y `@PASSWORD` con credenciales de un usuario registrado en Firebase.
3. Ejecute primero el bloque **INICIAR SESIÓN EN FIREBASE** (guarda el token en `@firebaseLogin`).
4. Ejecute luego los bloques de creación y consulta de empresas.

### Opción C — API con PowerShell / curl

1. Obtenga un ID token contra la API pública de Firebase Identity Toolkit:

```powershell
$body = @{ email = "usuario@correo.com"; password = "clave"; returnSecureToken = $true } | ConvertTo-Json
$login = Invoke-RestMethod -Method Post -Uri "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyAvrtadjsZgY8sJd-wulMxvL8zcKr2fbbg" -ContentType "application/json" -Body $body
$token = $login.idToken
```

2. Consulte las empresas del usuario:

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/api/companies/" -Headers @{ Authorization = "Bearer $token" }
```

3. Cree una empresa:

```powershell
$data = @{ name = "Mi Empresa"; nit = "900000000-1"; city = "Medellín"; sector = "Reciclaje" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/companies/" -Headers @{ Authorization = "Bearer $token" } -ContentType "application/json" -Body $data
```

### Opción D — Con Swagger UI (recomendado)

1. Inicie el backend y abra **http://127.0.0.1:8000/api/docs/**.
2. Obtenga un **ID token** de Firebase (en `firebase-materials-simple.http` el
   bloque "INICIAR SESIÓN" lo devuelve en `idToken`, o generándolo desde la
   consola del navegador con un usuario ya autenticado).
3. Pulse el botón **Authorize** y pegue el ID token (formato `Bearer <token>`).
4. Desde Swagger puede ejecutar `GET/POST /api/companies/` y `GET/POST /api/materials/`
   directamente, con el cuerpo de ejemplo ya documentado.

> Nota: los endpoints protegidos responden **401** si el token falta o expiró, y
> **403** si se invoca sin `Authorization`.

### Opción E — Registro con roles

Los perfiles se guardan en la colección **`users`** de MongoDB con la forma:

```json
{
  "uid": "<uid_firebase>",
  "email": "usuario@correo.com",
  "nombre": "Nombre",
  "role": "usuario | empresa | admin",
  "created_at": "2026-08-12T00:00:00+00:00"
}
```

**Roles disponibles:** `usuario`, `empresa` y `admin`.

Flujo de registro (el usuario primero se crea en Firebase desde el frontend):

1. El frontend llama a `createUserWithEmailAndPassword` de Firebase.
2. Con el usuario ya creado, el frontend obtiene el ID token.
3. El frontend llama a `POST /api/auth/register/` con el token y el cuerpo:

```json
{
  "nombre": "Nombre de la persona o empresa",
  "role": "empresa"
}
```

4. El backend toma el `uid` del token (nunca del cuerpo), valida que el rol sea
   `usuario` o `empresa` (el rol `admin` **no** se puede auto-registrar) y
   guarda el perfil. Si el perfil ya existe responde **409 Conflict**.

**Crear un administrador** (manual, no se auto-registra):

```bash
python manage.py seed_admin --uid "<uid_firebase>" --email "admin@correo.com" --nombre "Admin"
```

Una vez con rol `admin`, el usuario puede listar perfiles (`GET /api/users/`),
ver un perfil (`GET /api/users/{uid}/`) y cambiar roles
(`PATCH /api/users/{uid}/role/` con `{"role": "admin"}`).

> Nota: los módulos de empresas y materiales aún **no** restringen por rol
> (cualquier usuario autenticado puede usarlos). La regla de negocio "solo
> empresas publican" del contexto se puede aplicar como siguiente paso usando
> `users/permissions.py`.

---

## 9. Hallazgos, código faltante y riesgos

### Código faltante (bloquea pasos documentados)

1. **Resuelto** — los `__init__.py` de `companies/management/commands/` se
   crearon; `python manage.py seed_demo` ya funciona.

2. **Falta `frontend/.env`** — no existe; el frontend mostrará la pantalla de
   "Configuración incompleta" hasta crearlo (ver [sección 6.1](#61-crear-el-archivo-env)).
   Falta conocer `VITE_FIREBASE_APP_ID` (Firebase Console).

3. **Resuelto** — el registro de perfiles con roles (`usuario`/`empresa`) ya
   existe en `POST /api/auth/register/`. El usuario se crea primero en Firebase
   desde el frontend; el backend guarda el perfil con su rol.

### Riesgos de seguridad (importantes)

4. **`backend/.env` está versionado en git** y contiene la cadena de conexión de
   MongoDB Atlas con credenciales y el `DJANGO_SECRET_KEY`. Debe sacarse del
   control de versiones (`git rm --cached backend/.env`) y rotarse la contraseña
   de MongoDB.

5. **`backend/firebase-service-account.json` NO está realmente ignorado** — el
   archivo `backend/.gitignore` usa patrones con prefijo `backend/...`, pero el
   `.gitignore` ya vive dentro de `backend/`, por lo que `backend/.env`,
   `backend/venv/` y `backend/firebase-service-account.json` **no coinciden con
   nada**. Un `git add -A` subiría la clave privada de Firebase. Los patrones
   correctos son `.env`, `venv/`, `firebase-service-account.json`.

### Observaciones de código

6. **`config/urls.py` define `urlpatterns` dos veces** — el primer bloque
   (router + `health/`) es código muerto que queda sobrescrito por el segundo.
   Funciona (la URL efectiva es `/api/health/`), pero conviene eliminar el primer
   bloque para evitar confusiones.

7. **Los ViewSets solo implementan `list` y `create`** — no existen operaciones
   de consultar por id, editar ni eliminar para empresas ni materiales.

8. **Clave inconsistente `material-status`** — en
   `companies/views.py:105` el campo `status_Material` se guarda con guion
   (`"material-status"`), mientras el resto del documento usa `snake_case`.

9. **`seed_demo.py` inserta datos con `owner_uid: "demo-owner"`** — como las
   consultas filtran por el `uid` real de Firebase, esos datos demo no serán
   visibles para ningún usuario autenticado.

10. **Bug menor de UI en `CompanyForm.jsx`** — el campo "Sector económico" tiene
    repetido el rótulo "Tamaño" (línea ~106).

11. **Sin pruebas automatizadas** — `backend/companies/tests.py` y el frontend no
    tienen pruebas; solo validación estática (`manage.py check`, `npm run lint/build`).

---

## 10. Solución de problemas frecuentes

| Problema | Causa probable | Solución |
|---|---|---|
| El frontend muestra "Configuración incompleta" | No existe `frontend/.env` | Crearlo con los valores de la sección 6.1 |
| `Unknown command: 'seed_demo'` | (Resuelto) faltaban los `__init__.py` | Reiniciar el shell si se agregaron recién |
| `401 Unauthorized` en la API | Token ausente, inválido o vencido | Adjuntar `Bearer <idToken>` vigente |
| `403 Forbidden` en `/api/users/` | El usuario no tiene rol `admin` | Asignar rol con `seed_admin` o `PATCH role` |
| `409 Conflict` en `register` | El perfil ya existe para ese uid | Usar `GET /api/auth/me/` para consultarlo |
| `400` en `register` | Rol `admin` u otro no permitido | Usar `usuario` o `empresa` |
| Error de red/timeout con MongoDB | IP no autorizada en Atlas | **Atlas → Network Access →** agregar IP actual |
| `401` al iniciar sesión | Usuario no existe en Firebase | Crearlo en Firebase Console |
| CORS | Origen no permitido | Verificar `CORS_ALLOWED_ORIGINS` en `backend/.env` |

---

## 11. Referencias del proyecto

- Documentación del frontend: [`frontend/README.md`](frontend/README.md)
- Diagnóstico de pantalla blanca: [`frontend/docs/DIAGNOSTICO-PANTALLA-BLANCA.md`](frontend/docs/DIAGNOSTICO-PANTALLA-BLANCA.md)
- Guía de refactorización del frontend: [`frontend/docs/D-frontend-refactorizado.md`](frontend/docs/D-frontend-refactorizado.md)
