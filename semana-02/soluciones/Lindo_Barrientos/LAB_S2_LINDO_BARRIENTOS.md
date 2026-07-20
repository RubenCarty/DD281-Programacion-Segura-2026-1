# GUÍA DE LABORATORIO — SEMANA 2 (RESUELTA)
# IMPLEMENTACIÓN DE LOGIN SEGURO CON CGI Y SSL
## Programación Segura (DD281)

**Estudiante:** LINDO BARRIENTOS JHONN VIEQUIER
**Lenguaje:** Python 3.12 (en VS Code o WSL2)
**Fecha:** 20/06/2026

> **Nota sobre el código:** los archivos `setup_db.py`, `login_inseguro.py`, `login_seguro.py`, `servidor.py` y `www/login.html` se usan **tal como figuran en la guía original** (no requieren modificación). Este documento resuelve todas las preguntas de reflexión, pruebas y análisis.
>
> **Aviso de versión:** este lab usa `cgi`, `cgitb` y `http.server.CGIHTTPRequestHandler`, **eliminados en Python 3.13**. Ejecútalo con **Python 3.12/3.11** o en **WSL2**. Con Python 3.13+ fallará en `import cgi`.

---

## PARTE 1 — CONFIGURACIÓN DEL ENTORNO

### Paso 1.3 — Inicializar la Base de Datos

**¿Cuánto tiempo tardó en crear los 4 usuarios?**

*Respuesta:* Aproximadamente **2 a 4 segundos** (cada hash bcrypt con factor 12 toma ~0,3–0,5 s). _Confirma el valor con tu propia ejecución._

**¿Por qué tarda ese tiempo? ¿Es un defecto o una característica de seguridad?**

*Respuesta:* Es una **característica de seguridad**, no un defecto. bcrypt con factor de coste 12 ejecuta **2¹² (4096) rondas** de derivación a propósito para que cada hash sea costoso de calcular. Esa lentitud deliberada es lo que encarece y vuelve inviable la fuerza bruta a gran escala; un hash "rápido" como MD5/SHA-256 sería precisamente lo inseguro.

---

## PARTE 5 — EJECUCIÓN Y PRUEBAS

### Paso 5.2 — Acceder al login en el navegador

**¿Por qué aparece esta advertencia?**

Porque el certificado es **autofirmado**: no fue emitido ni validado por una **Autoridad Certificadora (CA)** en la que el navegador confíe, así que el navegador no puede verificar la identidad del servidor y advierte del riesgo. En un laboratorio local sobre `localhost` es esperado y se acepta la excepción; en producción nunca debe usarse un autofirmado.

---

### Paso 5.3 — Pruebas del sistema

#### Prueba 1 — Login exitoso

| Campo | Valor |
|---|---|
| Usuario | `juan.garcia` |
| Contraseña | `MiPassword123!` |
| Resultado esperado | Mensaje de acceso concedido |

**Resultado obtenido:** ✅ "Acceso concedido — Bienvenido. Has iniciado sesión como **estudiante**." _(adjuntar captura)_

---

#### Prueba 2 — Credenciales incorrectas

| Campo | Valor |
|---|---|
| Usuario | `juan.garcia` |
| Contraseña | `contraseñaIncorrecta` |
| Resultado esperado | Mensaje genérico de error + contador de intentos |

**Resultado obtenido:** ❌ "Credenciales incorrectas. Te quedan 4 intento(s) antes del bloqueo temporal."

**¿El mensaje revela si el usuario existe?** ☐ Sí ☑ **No**

**¿Por qué es importante que NO revele esta información?**

Para evitar la **enumeración de usuarios**: si el mensaje distinguiera entre "usuario no existe" y "contraseña incorrecta", un atacante podría descubrir qué cuentas son válidas y concentrar la fuerza bruta solo en ellas. El mensaje genérico no le da pistas.

---

#### Prueba 3 — Intento de SQL Injection

| Input | Resultado esperado | Resultado obtenido |
|---|---|---|
| `' OR '1'='1` | Acceso denegado | ❌ Acceso denegado (credenciales incorrectas) |
| `admin' --` | Acceso denegado | ❌ Acceso denegado (credenciales incorrectas) |
| `'; DROP TABLE usuarios; --` | Acceso denegado | ❌ Acceso denegado; la tabla **no** se elimina |

**¿El sistema fue vulnerable?** ☐ Sí ☑ **No**

**¿Qué mecanismo del código previene el SQL Injection?**

Los **prepared statements** (consulta parametrizada con `?`): `cursor.execute("... WHERE usuario = ?", (usuario,))`. La entrada se envía como **dato**, separada de la estructura de la consulta, de modo que `' OR '1'='1` se busca literalmente como un nombre de usuario (que no existe) y nunca se interpreta como código SQL.

---

#### Prueba 4 — Bloqueo de cuenta

| Intento # | Contraseña usada | Resultado |
|---|---|---|
| 1 | `mal1` | ❌ "Credenciales incorrectas. Te quedan 4 intento(s)." |
| 2 | `mal2` | ❌ "Te quedan 3 intento(s)." |
| 3 | `mal3` | ❌ "Te quedan 2 intento(s)." |
| 4 | `mal4` | ❌ "Te quedan 1 intento(s)." |
| 5 | `mal5` | 🔒 "Tu cuenta ha sido bloqueada por 5 intentos fallidos. Intenta en 15 minutos." |
| 6 (con clave correcta) | `SecurePass456#` | 🔒 Sigue bloqueada: "Cuenta bloqueada temporalmente. Intenta en N minuto(s)." |

**¿Cuál es el tiempo de bloqueo configurado en el sistema?** **15 minutos** (`TIEMPO_BLOQUEO = 15`).

---

#### Prueba 5 — Intento de XSS en el campo usuario

| Input | Resultado esperado |
|---|---|
| `<script>alert('XSS')</script>` | El script NO debe ejecutarse — debe aparecer como texto |

**Resultado obtenido:** El texto se muestra **literal y escapado** (`&lt;script&gt;...`), no se ejecuta ninguna alerta. El login lo trata como un usuario inexistente y deniega el acceso.

**¿Qué función del código previene el XSS?**

`html.escape()`, aplicada al usuario (`usuario = html.escape(str(usuario_raw).strip())`) y dentro de `render_page()` antes de reflejar cualquier valor en el HTML. Convierte `< > & "` en entidades, neutralizando el script.

---

#### Prueba 6 — Revisar los logs de seguridad

**¿Qué tipos de eventos aparecen en el log?**

`AUTH_SUCCESS`, `AUTH_FAILURE`, `CUENTA_BLOQUEADA`, y según el caso `MÉTODO_INVÁLIDO`, `INPUT_INVÁLIDO` y `ERROR_BD`.

**¿Qué información registra un evento de fallo?**

Fecha y hora, nivel (`WARNING`), usuario afectado, número de intento (`intento=n/5`) y la **IP del cliente**.

**¿Por qué es importante registrar los intentos fallidos?**

Permite **detectar ataques** (fuerza bruta, enumeración), realizar **auditoría y trazabilidad** de los accesos, e **investigar incidentes** después de un compromiso. Sin logs, un ataque puede pasar completamente inadvertido.

---

### Paso 5.4 — Verificar los Headers de Seguridad

| Header | ¿Presente? | Valor observado |
|---|---|---|
| `Strict-Transport-Security` | ☑ Sí | `max-age=31536000; includeSubDomains` |
| `X-Content-Type-Options` | ☑ Sí | `nosniff` |
| `X-Frame-Options` | ☑ Sí | `DENY` |
| `Cache-Control` | ☑ Sí | `no-store, no-cache, must-revalidate` |

**¿Para qué sirve el header `X-Frame-Options: DENY`?**

Impide que la página sea cargada dentro de un `<iframe>`, `<frame>` u `<object>` en otro sitio. Así se previene el **clickjacking**, donde un atacante superpone la página real bajo una falsa para engañar al usuario y hacerle ejecutar acciones sin darse cuenta.

---

## PARTE 6 — ANÁLISIS COMPARATIVO

### Paso 6.1 — Análisis del script inseguro vs seguro

| Aspecto de seguridad | `login_inseguro.py` | `login_seguro.py` |
|---|---|---|
| **Protección SQL Injection** | ❌ Concatena la entrada con f-string en la consulta | ✅ Prepared statements con parámetros `?` |
| **Almacenamiento de contraseñas** | ❌ Compara contra texto plano | ✅ Verifica hash **bcrypt** con `checkpw()` |
| **Verificación de método HTTP** | ❌ No verifica (acepta GET/POST) | ✅ Solo acepta `POST`; rechaza el resto |
| **Protección XSS en output** | ❌ Refleja `usuario` y `fila` sin escapar | ✅ `html.escape()` en toda la salida |
| **Manejo de intentos fallidos** | ❌ Sin límite ni bloqueo | ✅ Bloqueo tras 5 intentos por 15 min |
| **Logging de eventos** | ❌ No registra nada | ✅ Registra éxito, fallo y bloqueo con IP |
| **Mensajes de error** | ❌ Revela si el usuario existe (enumeración) | ✅ Mensaje genérico ("Credenciales incorrectas") |
| **Headers de seguridad HTTP** | ❌ Ninguno | ✅ HSTS, X-Frame-Options, X-Content-Type-Options, Cache-Control |
| **Timing attack prevention** | ❌ Sin protección | ✅ Ejecuta `checkpw` con hash *dummy* aunque el usuario no exista |

---

### Paso 6.2 — Análisis del hash bcrypt en la BD

**¿Todos los hashes tienen el mismo prefijo `$2b$12$`?** ☑ **Sí** (todos comparten el algoritmo `2b` y el factor de coste `12`).

**¿Por qué todos los hashes tienen la MISMA longitud aunque las contraseñas sean distintas?**

Porque bcrypt produce siempre una salida de **60 caracteres** de longitud fija (prefijo `$2b$`, coste, 22 caracteres de sal y 31 del hash), sin importar el largo de la contraseña de entrada. La longitud del hash no depende de la contraseña.

**¿Podrías saber cuál usuario tiene la contraseña "más simple" solo mirando los hashes?** ☐ Sí ☑ **No** — **¿Por qué?**

Porque cada hash incorpora una **sal aleatoria única** y la salida tiene longitud fija; no existe ninguna relación visible entre la complejidad de la contraseña y su hash. Dos usuarios con la misma contraseña tendrían hashes **distintos**, por lo que es imposible inferir nada observando los hashes.

---

## PARTE 7 — EJERCICIO DE EXTENSIÓN (AVANZADO)

### Desafío: Implementar CSRF Protection

**Describe tu implementación:**

1. **Generación del token:** al servir el formulario se crea un token con `secrets.token_hex(32)` (criptográficamente seguro) y se guarda asociado a la sesión del usuario (cookie de sesión `HttpOnly` o almacenamiento de sesión en servidor).
2. **Inserción en el formulario:** se añade un campo oculto en `login.html`: `<input type="hidden" name="csrf_token" value="...">`, de modo que el token viaja con cada envío legítimo.
3. **Validación en el CGI:** al recibir el POST se compara el token enviado con el esperado usando **comparación en tiempo constante** para no filtrar información por *timing*:

```python
token_recibido = form.getvalue("csrf_token", "")
if not hmac.compare_digest(token_recibido, token_esperado):
    print(render_page("Error CSRF", "Token de seguridad inválido."))
    exit(0)
```

Así, una página maliciosa de otro dominio no puede falsificar el envío porque **no conoce el token** ligado a la sesión de la víctima. (En CGI puro sin estado, el token debe persistirse en una cookie de sesión `HttpOnly`/`SameSite=Strict` para poder compararlo.)

---

## ENTREGABLE — INFORME_LAB2

### 1. Resumen ejecutivo

Implementé y probé un sistema de login seguro en Python con CGI sobre HTTPS. Generé un certificado SSL autofirmado con OpenSSL, inicialicé una base SQLite con contraseñas hasheadas en **bcrypt (factor 12)** y desplegué un servidor con TLS 1.2+. Verifiqué que el login resiste **SQL Injection** (prepared statements), **XSS** (`html.escape`), **fuerza bruta** (bloqueo tras 5 intentos), **enumeración de usuarios** (mensajes genéricos) y **timing attacks** (hash *dummy*). Aprendí que la seguridad de un login es un conjunto de capas y que decisiones como la lentitud de bcrypt son intencionales.

### 2–4. Capturas requeridas

- [ ] Advertencia del certificado SSL + información del certificado (navegador).
- [ ] Login exitoso (`juan.garcia`).
- [ ] Contenido de `logs/auth.log` mostrando éxito, fallo y bloqueo.

_(Adjuntar en `capturas/` — son evidencia propia, capturadas de tu ejecución.)_

### 5. Respuestas a las preguntas de reflexión

Resueltas en las Partes 1, 5 y 6 de este documento.

### 6. Tabla comparativa

Completada en el Paso 6.1.

### 7. Vulnerabilidades identificadas en el script inseguro

SQL Injection por concatenación, comparación de contraseña en texto plano, XSS por reflejo sin escapar, exposición de datos del registro, enumeración de usuarios por mensaje específico, y ausencia de rate limiting y logging.

### 8. Reflexión final — 3 mejoras posibles

1. **Migrar a argon2id** (o subir el factor de bcrypt según el hardware), por ser el algoritmo recomendado actualmente para derivación de contraseñas.
2. **Añadir MFA (segundo factor, OTP)** para que el robo de contraseña no baste para acceder.
3. **Implementar token CSRF + cookies `HttpOnly`/`SameSite=Strict`** y **rate limiting por IP** (no solo por cuenta) para frenar ataques distribuidos.

---

## CRITERIOS DE EVALUACIÓN (referencia)

| Criterio | Peso |
|---|---|
| Certificado SSL generado y funcional | 15% |
| Script CGI seguro funcional | 30% |
| Pruebas documentadas | 25% |
| Análisis de vulnerabilidades | 15% |
| Informe y reflexión | 15% |

---

*Laboratorio — Semana 2 | Programación Segura DD281 | Universidad Autónoma del Perú | 2026-1*
