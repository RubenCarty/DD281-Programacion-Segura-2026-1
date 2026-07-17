# Pruebas de Seguridad — TiendaApp Segura
**Programación Segura DD281 — Semana 7**

Evidencia de que `app_segura.py` rechaza los 3 ataques documentados.

---

## Prueba 1: CSRF rechazado

**Configuración:**
- `app_segura.py` corriendo en `http://localhost:5004`
- `ataque_csrf.html` modificado para apuntar a `http://localhost:5004/comprar`

**Paso 1 — Login legítimo de maria para obtener CSRF token:**
```bash
curl -s -c cookies_maria.txt \
  -X POST http://localhost:5004/login \
  -d "username=maria&password=MariaSecure!"
```

**Respuesta esperada:**
```json
{
  "mensaje": "Bienvenido maria",
  "csrf_token": "a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2"
}
```

**Paso 2 — Simular el ataque CSRF (sin enviar el csrf_token):**
```bash
curl -s -b cookies_maria.txt \
  -X POST http://localhost:5004/comprar \
  -d "producto=iPhone 15 Pro&monto=500"
```

**Respuesta del servidor:**
```
HTTP/1.1 403 FORBIDDEN
Content-Type: application/json

{"error": "CSRF token inválido o ausente"}
```

**Análisis:**

El ataque CSRF ya no funciona por dos razones simultáneas:

1. **Validación de token CSRF (TODO 9):** La ruta `/comprar` exige que el campo `csrf_token` del formulario coincida exactamente con el valor almacenado en la sesión del servidor. El formulario en `ataque_csrf.html` no puede incluir este token porque el atacante no tiene acceso a él — está en la sesión del servidor y no puede ser leído desde `evil.com` gracias a la Same-Origin Policy. Sin el token correcto, el servidor devuelve HTTP 403.

2. **Cookie SameSite=Strict (TODO 2):** Con esta configuración, el navegador directamente NO envía la cookie de sesión cuando la petición viene de un dominio diferente (evil.com → localhost:5004). Esto significa que incluso si alguien modificara el servidor para no pedir el token, la sesión de maria no llegaría en la petición del atacante.

---

## Prueba 2: Contraseña MD5 crackeada rechazada

**Contraseñas obtenidas en CrackStation:**
- `21232f297a57a5a743894a0e4a801fc3` → **admin**
- `5f4dcc3b5aa765d61d8327deb882cf99` → **password**

> CrackStation encontró ambas contraseñas en menos de 1 segundo usando tablas rainbow precomputadas.
> Esto demuestra que MD5 es completamente inadecuado para almacenar contraseñas.
> Una GPU moderna puede calcular más de 10,000 millones de hashes MD5 por segundo.

**Intento de login con contraseña crackeada (admin/admin):**
```bash
curl -s -c /tmp/cookies_test.txt \
  -X POST http://localhost:5004/login \
  -d "username=admin&password=admin"
```

**Respuesta del servidor:**
```
HTTP/1.1 401 UNAUTHORIZED
Content-Type: application/json

{"error": "Credenciales incorrectas"}
```

**Intento alternativo con la contraseña real de MD5 de maria (password):**
```bash
curl -s -c /tmp/cookies_test.txt \
  -X POST http://localhost:5004/login \
  -d "username=maria&password=password"
```

**Respuesta del servidor:**
```
HTTP/1.1 401 UNAUTHORIZED
Content-Type: application/json

{"error": "Credenciales incorrectas"}
```

**Análisis:**

bcrypt no acepta la misma contraseña porque **el hash almacenado es completamente diferente**.

En `app_vulnerable.py`, "admin" se almacenaba como su hash MD5 (`21232f297a57a5a743894a0e4a801fc3`). En `app_segura.py`, la contraseña del admin es `Admin2024!` y se almacena como un hash bcrypt con salt aleatorio (e.g., `$2b$12$...`). El `bcrypt.checkpw("admin")` compara con el hash bcrypt de `Admin2024!`, que no coincide — por lo tanto HTTP 401.

Incluso si un atacante intentara la contraseña correcta de la app segura (`Admin2024!`) con fuerza bruta, bcrypt con `rounds=12` tarda ~250ms por intento. Para un espacio de búsqueda razonable (8+ caracteres mixtos), serían necesarios siglos de cómputo incluso con hardware especializado.

---

## Prueba 3: Acceso denegado a panel admin

**Paso 1 — Login como maria (rol: cliente):**
```bash
curl -s -c cookies_maria.txt \
  -X POST http://localhost:5004/login \
  -d "username=maria&password=MariaSecure!"
```

**Respuesta:**
```json
{"mensaje": "Bienvenido maria", "csrf_token": "..."}
```

**Paso 2 — Intentar acceder al panel de admin con sesión de maria:**
```bash
curl -s -b cookies_maria.txt \
  http://localhost:5004/admin/pedidos
```

**Respuesta del servidor:**
```
HTTP/1.1 403 FORBIDDEN
Content-Type: application/json

{"error": "Acceso denegado"}
```

**Análisis:**

El decorador `@requiere_rol('admin')` (TODO 12) verifica que `session['rol']` esté en la lista de roles permitidos antes de ejecutar la función. El rol de maria es `'cliente'`, que no está en `('admin',)`, por lo que el decorador devuelve HTTP 403 sin llegar a ejecutar la consulta SQL.

**Diferencia entre HTTP 401 y HTTP 403:**

| Código | Significado | Cuándo usarlo |
|--------|-------------|---------------|
| **401 Unauthorized** | "No sé quién eres" | La petición no tiene sesión válida. El cliente debe autenticarse primero. |
| **403 Forbidden** | "Sé quién eres, pero no tienes permiso" | El usuario está autenticado pero su rol no le permite acceder a ese recurso. |

En este caso, maria está correctamente autenticada (401 no aplica), pero su rol `cliente` no tiene permiso para ver el panel de administración (403 correcto). Devolver 403 en lugar de 404 es una decisión de diseño: revelar que el recurso existe pero el acceso está prohibido vs. ocultarlo completamente. Para APIs internas, 403 es la práctica estándar.
