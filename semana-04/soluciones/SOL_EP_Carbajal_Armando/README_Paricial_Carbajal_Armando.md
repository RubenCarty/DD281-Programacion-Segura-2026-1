# 🚀 UQ AI Intranet - Sistema Seguro de Captura e Inspección de Leads comerciales

¡Proyecto Parcial Finalizado con éxito! Una plataforma corporativa distribuida y blindada bajo estándares modernos de ciberseguridad industrial y desarrollo guiado por buenas prácticas de arquitectura.

---

## 👤 Información del Autor
* **Desarrollador:** Armando Jheferson Carbajal Campomanes
* **Proyecto:** Solución Integral de Intranet Segura y Automatización con Inteligencia Artificial
* **Ámbito:** Examen Parcial - Ingeniería de Sistemas

---

## 🌐 Enlaces Oficiales del Despliegue

| Componente | Tipo de Recurso | Enlace de Acceso |
| :--- | :--- | :--- |
| **Frontend (Next.js)** | Despliegue en Producción | [Visitar Aplicación en Vercel](https://uqai-intranet.vercel.app/) |
| **Código Fuente** | Repositorio Público | [Ver en GitHub](https://github.com/acarbajalCode/UQAIIntranet.git) |
| **Demostración** | Video Explicativo | [Ver Video de Sustentación](https://drive.google.com/file/d/1h0W47LA_nGurJNpNZNC3D5mCXnA65-en/view?usp=sharing) |

---

## 📋 Resumen Ejecutivo de la Solución Aplicada

El sistema resuelve la necesidad corporativa de automatizar de forma segura la captación de prospectos comerciales externos desde una página de aterrizaje (Landing Page), procesarlos mediante una arquitectura aislada, y disponibilizarlos exclusivamente a personal auditado y autenticado.

### 🛡️ Pilares Tecnológicos y Seguridad Implementada
* **Arquitectura de Entornos Distribuidos:** Separación física del Frontend (alojado a nivel global en la red de Vercel) y el Backend (corriendo de manera independiente en los servidores de Railway).
* **Blindaje de Sesiones en el Servidor:** La autenticación utiliza una estrategia basada en Tokens seguros inyectados directamente a través de **Cookies con la propiedad `HttpOnly`**. Esto evita que el token sea accesible por scripts maliciosos en el navegador, mitigando ataques de tipo XSS.
* **Control de Accesos por Roles (RBAC):** El sistema discrimina dinámicamente las rutas. Los operadores comunes (`USER`) solo acceden a funciones operativas, mientras que el listado analítico de solicitudes está estrictamente reservado para cuentas autorizadas con rol de **`ADMIN`**.
* **Gestión de Datos Aislada y Segura:** Implementación de persistencia de datos relacional y ágil en memoria para aislar de forma segura los entornos de producción reales de las fases previas de desarrollo.

---

## 📂 Evidencias y Auditoría en la Raíz del Proyecto

Como respaldo técnico de la calidad del software y su correcto funcionamiento dinámico de extremo a extremo, se han adjuntado **dos archivos PDF obligatorios** en la carpeta principal de este repositorio:

  1. **`Evidencias_Pruebas_Postman_CARBAJAL_Armando.pdf`** Contiene el flujo completo de auditoría y testeo de la API REST de forma dinámica: Registro de operadores, validación segura de inicios de sesión, envío público de solicitudes de contacto y la denegación/aprobación de acceso basada en roles (`403 Forbidden` vs `200 OK`).
2. **`Evidencias_Consola_H2_Database_CARBAJAL_Armando.pdf`** Muestra el acceso en vivo y el monitoreo interno directo sobre la base de datos relacional en memoria dentro del servidor de Railway, validando las inserciones de datos y la actualización dinámica de perfiles administrativos mediante sentencias SQL.
