# Respuestas — Laboratorio S3 (Sesiones Seguras y RBAC en Flask)

**Estudiante:** Jhonn Viequier Lindo Barrientos
**Curso:** Programación Segura (DD281) — Semana 3

---

## PARTE 1 — Exploración

**P1.1 — ¿Qué valor tiene la cookie `session` en DevTools? ¿Es el email directamente?**

No. No es el email en texto plano. Flask serializa el contenido de la sesión y lo **firma con `SECRET_KEY`** (HMAC); lo que aparece es una cadena codificada en base64 con su firma. La firma impide que el usuario **modifique** la sesión (si la altera, la firma no valida). Por eso no se guardan datos secretos ahí: el contenido es legible (no cifrado), pero no falsificable.

**P1.2 — ¿Qué pasa si cambias `SESSION_COOKIE_HTTPONLY` a `False`?**

En DevTools (Application → Cookies) la columna **HttpOnly deja de estar marcada**. La cookie queda **accesible desde JavaScript**, por lo que una vulnerabilidad XSS podría leer el session ID y robar la sesión. Con `True`, la marca aparece y el acceso por script queda bloqueado.

**P1.3 — Ejecuta `document.cookie` en la consola. ¿Qué muestra? ¿Por qué?**

Con `HttpOnly = True`, `document.cookie` **no muestra la cookie de sesión** (devuelve vacío o solo cookies no-HttpOnly). Esto ocurre precisamente porque `HttpOnly` impide que el JavaScript del navegador acceda a esa cookie, que es la defensa clave contra el robo de sesión vía XSS.

---

## PARTE 2 — Aplicación (RBAC)

### Tabla de pruebas (resultados reales verificados)

| Prueba | Usuario | Ruta | Resultado esperado | Resultado real |
|---|---|---|---|---|
| 1 | usuario@test.com | `/reportes` | 403 Acceso denegado | ✅ **403** |
| 2 | supervisor@test.com | `/reportes` | 200 OK — muestra reportes | ✅ **200** |
| 3 | usuario@test.com | `/admin/panel` | 403 Acceso denegado | ✅ **403** |
| 4 | admin@test.com | `/admin/panel` | 200 OK — panel admin | ✅ **200** |
| 5 | Sin login | `/dashboard` | Redirige a /login | ✅ **302 → /login** |

**Pregunta 2.1 — ¿Y si verificaras el rol con `request.args.get('role') == 'admin'`?**

Sería una vulnerabilidad grave de **control de acceso roto / parameter tampering**: el rol vendría del **cliente** (la URL). Un atacante simplemente añadiría `?role=admin` a la petición (`/admin/panel?role=admin`) y bypassearía el control sin ser administrador. Por eso el rol **debe leerse del servidor** (`session.get('user_role')`), que el usuario no puede modificar porque la sesión está firmada.

**Pregunta 2.2 — ¿El error 403 revela información del servidor?**

La página `error.html` muestra el mensaje "Acceso denegado. Requiere uno de: (...)", que expone **los roles exigidos** por la ruta —información mínima, pero más de la necesaria—. En producción conviene un mensaje genérico ("No tienes permiso") y **`debug=False`**, porque con `debug=True` Flask podría mostrar trazas internas (rutas, variables) ante un error no controlado.

---

## PARTE 3 — Desafío

**Desafío 3.1 — Observación de `/demo/fixation` antes y después del login**

Antes del login, `/demo/fixation` muestra un `session_id` (o "Sin sesión previa"). Después de autenticarse, el `session_id` **cambia por completo**, porque en el login se ejecuta `session.clear()`, que regenera la sesión. Esto demuestra la **prevención de Session Fixation**: si un atacante hubiera fijado un ID antes del login, ese ID queda inservible tras autenticarse.

**Reflexión final**

> _Respuesta personal — adáptala a tu experiencia._

El concepto que me costó más implementar fue la **prevención de Session Fixation**, porque no era evidente que bastara una línea (`session.clear()`) ubicada en el momento exacto —antes de asignar los datos del usuario— para neutralizar el ataque; entender *por qué* ahí y no después fue lo difícil. El que creo que tendrá mayor impacto en mi proyecto del curso es el **RBAC con verificación del rol desde el servidor**, porque define quién puede hacer qué en todo el sistema y, si se lee mal (desde el cliente), abre la puerta a escalamiento de privilegios. Sumado a las cookies `HttpOnly`/`Secure`/`SameSite`, forma la base de una gestión de sesiones defendible. Es la pieza que más superficie de ataque cubre con menos código.

---

## Verificación de atributos de cookie (para la rúbrica)

En la respuesta de login, la cabecera `Set-Cookie` incluye:
- ✅ `HttpOnly` — JavaScript no puede leer la cookie.
- ✅ `SameSite=Lax` — mitiga CSRF en peticiones cross-site.
- `Secure` — desactivado en desarrollo local (HTTP); se activa con `SESSION_COOKIE_SECURE=True` en producción (HTTPS).

Estado de los 6 TODO: **TODO 1** (config de cookies), **TODO 2** (`session.clear()` anti-fixation), **TODO 3** (logout servidor+cliente), **TODO 4** (panel admin con lista de usuarios), **TODO 5** (eliminar usuario con validaciones), **TODO 6** (auditoría de sesiones activas) — todos implementados en `app.py`.
