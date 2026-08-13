# Diagnóstico de pantalla blanca

## Causa identificada

El frontend requiere cinco variables de entorno durante el arranque:

```env
VITE_API_URL=
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_PROJECT_ID=
VITE_FIREBASE_APP_ID=
```

Cuando el archivo `.env` no existe o contiene valores vacíos, Firebase no puede
inicializarse. En una implementación que lanza la excepción durante la carga de
módulos, React no alcanza a montar componentes dentro de `#root`; por eso el
navegador muestra una página vacía.

## Corrección incorporada

1. La entrega incluye la configuración `.env` utilizada por el proyecto de
   referencia.
2. `main.jsx` valida las variables antes de importar la aplicación.
3. Si falta alguna variable, se muestra una pantalla de diagnóstico con sus
   nombres en vez de dejar la página en blanco.
4. Después de modificar `.env`, Vite debe reiniciarse.

## Ejecución

```bash
npm install
npm run dev
```

El backend debe estar activo en la URL indicada por `VITE_API_URL`.
