/**
 * Nombres de las variables de entorno obligatorias para ejecutar el frontend.
 *
 * Vite solo expone al navegador las variables cuyo nombre comienza por VITE_.
 */
export const REQUIRED_ENV_VARIABLES = Object.freeze([
  "VITE_API_URL",
  "VITE_FIREBASE_API_KEY",
  "VITE_FIREBASE_AUTH_DOMAIN",
  "VITE_FIREBASE_PROJECT_ID",
  "VITE_FIREBASE_APP_ID",
]);

/**
 * Valores leídos de import.meta.env.
 *
 * No se lanza una excepción durante la importación del módulo. Esto permite que
 * main.jsx muestre un diagnóstico visible cuando la configuración está
 * incompleta, en lugar de dejar el elemento #root vacío.
 */
const rawEnv = Object.freeze({
  VITE_API_URL: import.meta.env.VITE_API_URL,
  VITE_FIREBASE_API_KEY: import.meta.env.VITE_FIREBASE_API_KEY,
  VITE_FIREBASE_AUTH_DOMAIN: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  VITE_FIREBASE_PROJECT_ID: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  VITE_FIREBASE_APP_ID: import.meta.env.VITE_FIREBASE_APP_ID,
});

/**
 * Normaliza un valor de configuración como texto sin espacios laterales.
 */
function normalize(value) {
  return typeof value === "string" ? value.trim() : "";
}

/**
 * Devuelve las variables obligatorias que no tienen un valor configurado.
 */
export function getMissingEnvironmentVariables() {
  return REQUIRED_ENV_VARIABLES.filter((name) => !normalize(rawEnv[name]));
}

/**
 * Indica si el frontend cuenta con toda la configuración mínima de arranque.
 */
export function isEnvironmentConfigured() {
  return getMissingEnvironmentVariables().length === 0;
}

/**
 * Configuración centralizada consumida por Firebase y por el cliente HTTP.
 *
 * main.jsx valida primero los valores. Por ello, los módulos funcionales solo
 * se importan cuando este objeto contiene una configuración completa.
 */
export const env = Object.freeze({
  apiUrl: normalize(rawEnv.VITE_API_URL).replace(/\/+$/, ""),
  firebase: Object.freeze({
    apiKey: normalize(rawEnv.VITE_FIREBASE_API_KEY),
    authDomain: normalize(rawEnv.VITE_FIREBASE_AUTH_DOMAIN),
    projectId: normalize(rawEnv.VITE_FIREBASE_PROJECT_ID),
    appId: normalize(rawEnv.VITE_FIREBASE_APP_ID),
  }),
});
