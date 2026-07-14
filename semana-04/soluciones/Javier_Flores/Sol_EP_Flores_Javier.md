# UQ AI Solution 🚀
Por: Javier Flores Condeña

Este proyecto es una solución web full-stack desacoplada, diseñada para la gestión automatizada de prospectos (leads) y la autenticación segura de usuarios mediante el uso de Inteligencia Artificial. La arquitectura divide el **Frontend** (desplegado de forma estática en Vercel) y el **Backend** (una API REST robusta escalada en Railway).

## 🔗 Enlaces del Proyecto
* **Repositorio GitHub:** [https://github.com/J4v13rFl0r3s/uq-ai-solution.git](https://github.com/J4v13rFl0r3s/uq-ai-solution.git)

* **Url Proyecto:** https://uq-ai-solution-m3yw.vercel.app/

* **Demostración en Video:** [Ver video explicativo en Google Drive](https://drive.google.com/file/d/1fTgjU3zlyHpdrfPUo5S0YQBuqbv_cVIU/view)

---

## 🛠️ Arquitectura y Flujo de Desarrollo

La aplicación se construyó bajo un enfoque de **arquitectura limpia y desacoplada**, facilitando el mantenimiento independiente de ambas capas:

### 1. Frontend (Desplegado en Vercel)
* **Tecnología y Diseño:** La interfaz web cuenta con un diseño oscuro (*Dark Mode*) de alta fidelidad, enfocado en la conversión, con formularios reactivos para la captura ágil de prospectos.
* **Infraestructura:** Se utilizó **Vercel** para aprovechar su red de distribución de contenidos (CDN) global, garantizando tiempos de carga óptimos y despliegue continuo (CI/CD) directo desde GitHub.

### 2. Backend (Desplegado en Railway)
* **Tecnología:** API REST funcional estructurada mediante controladores (`AuthController`, `LeadController`, `UsuarioController`).
* **Infraestructura:** Se seleccionó **Railway** debido a su soporte nativo para entornos de ejecución de servidores persistentes, gestión ágil de variables de entorno y recarga automatizada.
* **Disponibilidad:** Incluye un `HealthController` (`GET /health`) para monitorización continua y aseguramiento del uptime en el contenedor.

---

## 🛡️ Implementación y Puntos de Seguridad Aplicados

El proyecto fue diseñado siguiendo buenas prácticas de desarrollo seguro para proteger la integridad de los datos de los usuarios y evitar accesos no autorizados:

1. **Protección de Sesión mediante Cookies `HttpOnly`:**
   * En lugar de almacenar los tokens de acceso en el almacenamiento local del navegador (`LocalStorage`), el backend emite el JWT embebido en una cookie con el flag `HttpOnly`. 
   * Esto bloquea por completo el acceso al token mediante scripts de JavaScript en el cliente, mitigando drásticamente el riesgo de ataques de **Cross-Site Scripting (XSS)** y robo de credenciales.

2. **Autenticación y Autorización basada en Roles (RBAC):**
   * El sistema diferencia estrictamente los niveles de acceso entre usuarios convencionales (`USER`) y administradores (`ADMIN`).
   * Los endpoints críticos que exponen información sensible (como el listado general de prospectos y la base de usuarios) están protegidos mediante middlewares de verificación que validan la firma del JWT y exigen explícitamente el rol de administrador.

3. **Mecanismo de Bloqueo Anti-Fuerza Bruta:**
   * La pantalla de inicio de sesión cuenta con una política de seguridad activa que ejecuta un **bloqueo temporal tras 3 intentos fallidos** de autenticación. Esto previene ataques automatizados de diccionario o fuerza bruta dirigidos a adivinar contraseñas de cuentas.

4. **Políticas de Cifrado y Comunicación Segura:**
   * Toda la transferencia de datos viaja cifrada de extremo a extremo a través del protocolo seguro **HTTPS** provisto por los proxies inversos de Vercel y Railway.
   * Las contraseñas de los usuarios no se almacenan en texto plano en la base de datos; pasan por una función de derivación de claves mediante algoritmos de hash seguros antes de ser persistidas.

---

## 🔑 Matriz de Endpoints Funcionales

La API expone un total de 6 endpoints clave para la operación de la plataforma:

| # | Método | Ruta | Acceso | Función |
|---|---|---|---|---|
| **1** | `POST` | `/api/auth/register` | Público | Registrar un usuario (Campos en español; rol por defecto `USER`). |
| **2** | `POST` | `/api/auth/login` | Público | Iniciar sesión. Valida credenciales, aplica control de intentos y genera el JWT. |
| **3** | `POST` | `/api/leads` | Público | Registra los datos del formulario de contacto directamente al panel. |
| **4** | `GET` | `/api/leads` | Solo ADMIN | Listar la totalidad de prospectos registrados (Panel interno protegido). |
| **5** | `GET` | `/api/usuarios` | Solo ADMIN | Listar todos los usuarios del sistema. |
| **6** | `GET` | `/api/usuarios/{id}` | ADMIN / Propio USER | Ver la información detallada del perfil correspondiente. |

---

## 📋 Ejemplos de Estructura de Datos (JSON)

### Registro de Usuario (`POST /api/auth/register`)
Los campos obligatorios de la lógica de negocio se procesan estrictamente en español:
```json
{
  "nombre": "Javier",
  "apellidos": "Flores Condeña",
  "email": "javier@uqaisolution.com",
  "password": "MiClave123",
  "rol": "ADMIN",
  "area": "Sistemas"
}