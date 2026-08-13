# Frontend React refactorizado

Frontend de la aplicación de gestión de empresas y publicaciones de materiales. El proyecto conserva los contratos HTTP del código original y reorganiza la solución mediante módulos funcionales, servicios especializados, autenticación centralizada y componentes reutilizables.

## Inicio rápido

```bash
npm install
npm run dev
```

Esta entrega incluye un archivo `.env` funcional tomado de la configuración suministrada para las pruebas locales. Si se crea el proyecto en otro equipo o se elimina ese archivo, copie `.env.example` como `.env`, complete las variables de Firebase y reinicie Vite. El backend debe estar disponible en la URL definida por `VITE_API_URL`.

## Validación técnica

```bash
npm run lint
npm run build
# o ambas verificaciones
npm run check
```

## Contratos conservados

| Operación | Método | Endpoint |
|---|---:|---|
| Consultar empresas | GET | `/companies/` |
| Crear empresa | POST | `/companies/` |
| Consultar materiales | GET | `/materials/` |
| Crear material | POST | `/materials/` |

Todas las llamadas se realizan sobre `VITE_API_URL` y adjuntan un token Firebase vigente en la cabecera `Authorization: Bearer <token>`.

## Estructura

```text
src/
├── app/                         # Composición global y rutas
├── config/                      # Variables de entorno y Firebase
├── features/                    # Módulos funcionales
│   ├── auth/
│   ├── companies/
│   ├── home/
│   └── materials/
├── shared/                      # Componentes, layout, servicios y utilidades comunes
├── styles/                      # Estilos globales
└── main.jsx                     # Punto de entrada
```

## Decisiones principales

- Firebase administra la persistencia de sesión; no se guarda manualmente el ID token en `localStorage`.
- `onAuthStateChanged` determina el usuario real antes de habilitar rutas privadas.
- El interceptor de Axios solicita un ID token vigente antes de cada petición.
- Las páginas coordinan casos de uso; los formularios presentan la interfaz y los servicios encapsulan HTTP.
- Las rutas se cargan con `lazy` y `Suspense`.
- `.env` permanece excluido del repositorio por `.gitignore`; se incorpora únicamente en esta entrega de prueba para conservar la configuración local suministrada.
- El arranque valida las variables obligatorias y muestra un diagnóstico visible en lugar de una pantalla blanca.
- `node_modules` queda excluido y debe reconstruirse con `npm install`.

## Documentación paso a paso

Consulte [`docs/D-frontend-refactorizado.md`](docs/D-frontend-refactorizado.md).
