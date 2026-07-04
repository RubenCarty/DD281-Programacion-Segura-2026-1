# LABORATORIO EN CASA — SEMANA 7
## Programación Segura DD281 | Universidad Autónoma del Perú
**Tema:** CSRF, Exposición de Datos Sensibles y Controles de Acceso
**Tiempo estimado:** 2 horas
**Modalidad:** Individual
**Entrega:** Repositorio GitHub → semana-07/lab-casa/
**Puntaje:** 100 puntos

---

## SOFTWARE REQUERIDO

- Python 3.10+: https://www.python.org/downloads/
- Instalar dependencias: `pip install flask flask-wtf bcrypt python-dotenv`
- Verificación: `python -c "import flask, flask_wtf, bcrypt; print('OK')"`
- Alternativa online: replit.com (crear proyecto Python)

---

## PARTE 1 — EXPLORACIÓN (30 min, 25 pts)

**Escenario:** TiendaApp es una aplicación de e-commerce con CSRF vulnerable.

**Código base `app_vulnerable.py`:**

```python
from flask import Flask, request, session, jsonify, redirect
import sqlite3, hashlib, os

app = Flask(__name__)
app.secret_key = "tienda2024"
# Sin SameSite, sin HttpOnly

def get_db():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    conn.executescript('''
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password_hash TEXT,
            saldo REAL,
            rol TEXT DEFAULT 'cliente'
        );
        CREATE TABLE pedidos (
            id INTEGER PRIMARY KEY,
            usuario_id INTEGER,
            producto TEXT,
            monto REAL
        );
        INSERT INTO usuarios VALUES (1, 'admin', '21232f297a57a5a743894a0e4a801fc3', 1000.0, 'admin');
        INSERT INTO usuarios VALUES (2, 'maria', '5f4dcc3b5aa765d61d8327deb882cf99', 500.0, 'cliente');
        INSERT INTO pedidos VALUES (1, 1, 'Laptop', 2500.0);
        INSERT INTO pedidos VALUES (2, 2, 'Mouse', 50.0);
    ''')
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    password_md5 = hashlib.md5(password.encode()).hexdigest()
    
    conn = get_db()
    user = conn.execute(
        f"SELECT * FROM usuarios WHERE username='{username}' AND password_hash='{password_md5}'"
    ).fetchone()
    conn.close()
    
    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['rol'] = user['rol']
        return jsonify({"mensaje": f"Bienvenido {user['username']}", "saldo": user['saldo']})
    return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route('/comprar', methods=['POST'])
def comprar():
    if not session.get('user_id'):
        return jsonify({"error": "No autenticado"}), 401
    
    # Sin CSRF token
    producto = request.form.get('producto')
    monto = float(request.form.get('monto', 0))
    
    conn = get_db()
    conn.execute(
        f"UPDATE usuarios SET saldo=saldo-{monto} WHERE id={session['user_id']}"
    )
    conn.execute(
        f"INSERT INTO pedidos (usuario_id, producto, monto) VALUES ({session['user_id']}, '{producto}', {monto})"
    )
    conn.commit()
    conn.close()
    return jsonify({"comprado": producto, "monto": monto})

@app.route('/admin/pedidos')
def listar_pedidos():
    # Sin verificación de rol
    conn = get_db()
    pedidos = conn.execute("SELECT * FROM pedidos").fetchall()
    conn.close()
    return jsonify([dict(p) for p in pedidos])

@app.route('/perfil')
def perfil():
    if not session.get('user_id'):
        return jsonify({"error": "No autenticado"}), 401
    conn = get_db()
    user = conn.execute(
        "SELECT id, username, saldo, rol FROM usuarios WHERE id=?",
        (session['user_id'],)
    ).fetchone()
    conn.close()
    return jsonify(dict(user))

if __name__ == '__main__':
    app.run(debug=True, port=5003)
```

---

### Tarea 1.1 (10 pts) — Análisis de vulnerabilidades

Analiza el código y completa esta tabla. Debes identificar **al menos 5 vulnerabilidades**:

| Línea/Función | Vulnerabilidad | OWASP | Riesgo | ¿Cómo se explota? |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

**Pistas de análisis:**
- ¿Qué ocurre si el atacante escribe `' OR '1'='1'--` en el campo username?
- ¿Qué tan seguro es MD5 para almacenar contraseñas en 2024?
- ¿Puede cualquier persona autenticada llamar a `/admin/pedidos`?
- ¿Qué impide que un sitio malicioso envíe un POST a `/comprar` en nombre del usuario?
- ¿Las cookies tienen la protección adecuada contra acceso desde JavaScript?

---

### Tarea 1.2 (10 pts) — Archivo del atacante

Crea el archivo `ataque_csrf.html` que un atacante usaría para forzar a maria (autenticada en TiendaApp) a realizar una compra de "iPhone 15 Pro" por S/. 500 desde evil.com.

El HTML debe cumplir estos requisitos:
- Ejecutarse **automáticamente** al cargar la página (sin que la víctima haga clic en nada)
- Estar **comentado línea a línea** explicando qué hace cada parte del código
- Incluir una **explicación al final** (en comentarios HTML): ¿por qué funciona este ataque si maria no hizo nada?

**Contexto del ataque:**
- TiendaApp corre en `http://localhost:5003`
- El archivo del atacante está alojado en `http://evil.com/oferta.html`
- Maria tiene una sesión activa en TiendaApp (cookie de sesión válida)
- El navegador de Maria enviará automáticamente las cookies de TiendaApp al hacer el POST

---

### Tarea 1.3 (5 pts) — Cracking de contraseñas MD5

Las contraseñas en la base de datos son:
- `21232f297a57a5a743894a0e4a801fc3` (usuario admin)
- `5f4dcc3b5aa765d61d8327deb882cf99` (usuario maria)

**Pasos:**
1. Ve a https://crackstation.net
2. Pega ambos hashes (uno por línea)
3. Haz clic en "Crack Hashes"
4. Toma una captura de pantalla del resultado

**Responde en tu entrega:**
- ¿Cuáles son las contraseñas reales?
- ¿Cuánto tiempo tardó CrackStation en encontrarlas?
- ¿Qué te dice esto sobre usar MD5 para almacenar contraseñas en producción?
- ¿Cuántos intentos por segundo puede hacer un atacante con GPU moderna crackeando MD5?

---

## PARTE 2 — IMPLEMENTACIÓN SEGURA (60 min, 50 pts)

Crea `app_segura.py` completando **todos los TODOs**. Para cada TODO debes agregar un comentario explicando qué vulnerabilidad previene y por qué es necesario.

```python
from flask import Flask, request, session, jsonify, redirect, make_response
import sqlite3, bcrypt, secrets, os, re
from functools import wraps
from dotenv import load_dotenv

load_dotenv()  # Carga variables de .env

app = Flask(__name__)

# TODO 1: Leer SECRET_KEY de variable de entorno; si no existe, generar con secrets.token_hex(32)
# Vulnerabilidad que previene: _______________
# Por qué es necesario: _______________
app.secret_key = "COMPLETAR"

# TODO 2: Configurar las 3 propiedades de seguridad de cookie de sesión
# Vulnerabilidad que previene: _______________
# Por qué es necesario: _______________
# SESSION_COOKIE_HTTPONLY = ?
# SESSION_COOKIE_SECURE = ?
# SESSION_COOKIE_SAMESITE = ?


def get_db():
    # Misma función que app_vulnerable.py pero con contraseñas bcrypt
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    
    # Generar hashes bcrypt correctos
    admin_hash = bcrypt.hashpw(b'Admin2024!', bcrypt.gensalt(rounds=12))
    maria_hash = bcrypt.hashpw(b'MariaSecure!', bcrypt.gensalt(rounds=12))
    
    conn.executescript(f'''
        CREATE TABLE usuarios (id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT, saldo REAL, rol TEXT);
        CREATE TABLE pedidos (id INTEGER PRIMARY KEY, usuario_id INTEGER, producto TEXT, monto REAL);
        INSERT INTO usuarios VALUES (1, 'admin', '{admin_hash.decode()}', 1000.0, 'admin');
        INSERT INTO usuarios VALUES (2, 'maria', '{maria_hash.decode()}', 500.0, 'cliente');
        INSERT INTO pedidos VALUES (1, 1, 'Laptop', 2500.0);
        INSERT INTO pedidos VALUES (2, 2, 'Mouse', 50.0);
    ''')
    return conn

def requiere_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({"error": "No autenticado"}), 401
        return f(*args, **kwargs)
    return decorated

def requiere_rol(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # TODO 3: Verificar autenticación (no user_id en session → 401)
            # Vulnerabilidad que previene: _______________
            
            # TODO 4: Verificar que session['rol'] está en roles (si no → 403)
            # Vulnerabilidad que previene: _______________
            
            return f(*args, **kwargs)
        return decorated
    return decorator

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    # TODO 5: Validar username con regex (solo letras, números, guiones bajos, guiones, 3-30 chars)
    # Vulnerabilidad que previene: _______________
    # Pista: usa re.match(r'^[a-zA-Z0-9_-]{3,30}$', username)
    
    conn = get_db()
    # TODO 6: Consulta parametrizada (no f-string con username)
    # Vulnerabilidad que previene: SQL Injection
    # Pista: usa "?" como placeholder y pasa una tupla (username,) como segundo argumento
    user = None  # REEMPLAZAR con la consulta parametrizada correcta
    conn.close()
    
    if user:
        # TODO 7: Verificar contraseña con bcrypt.checkpw()
        # Vulnerabilidad que previene: _______________
        # Pista: bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8'))
        pass
        
        # TODO 8: Limpiar session y regenerar (session.clear() antes de guardar datos de usuario)
        # Vulnerabilidad que previene: Session Fixation
        session['user_id'] = None  # COMPLETAR: asignar el id real del usuario
        
        # Generar CSRF token para esta sesión
        session['csrf_token'] = secrets.token_hex(32)
        
        return jsonify({"mensaje": f"Bienvenido"})
    return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route('/comprar', methods=['POST'])
@requiere_login
def comprar():
    # TODO 9: Validar CSRF token
    # Vulnerabilidad que previene: CSRF
    # Pista: comparar request.form.get('csrf_token') con session.get('csrf_token')
    # Si no coinciden → return jsonify({"error": "..."}), 403
    
    # TODO 10: Validar que monto sea float positivo y > 0
    # Vulnerabilidad que previene: _______________
    # Pista: usar try/except para convertir a float y verificar > 0
    
    producto = request.form.get('producto', '').strip()
    monto = 0.0  # REEMPLAZAR con el valor validado del TODO 10
    
    conn = get_db()
    # TODO 11: Consultas parametrizadas para UPDATE e INSERT (no f-strings)
    # Vulnerabilidad que previene: SQL Injection
    # Para el UPDATE: usa (monto, session['user_id']) — nunca tomes el user_id del request
    conn.close()
    
    # Regenerar CSRF token después de cada uso exitoso
    session['csrf_token'] = secrets.token_hex(32)
    
    return jsonify({"comprado": producto, "monto": monto})

@app.route('/admin/pedidos')
# TODO 12: Agregar decorador @requiere_rol('admin') aquí
# Vulnerabilidad que previene: Broken Access Control / falta de RBAC
def listar_pedidos():
    conn = get_db()
    pedidos = conn.execute("SELECT * FROM pedidos").fetchall()
    conn.close()
    return jsonify([dict(p) for p in pedidos])

@app.after_request
def headers_seguridad(response):
    # TODO 13: Agregar Content-Security-Policy
    # Valor: "default-src 'self'; script-src 'self'"
    # Vulnerabilidad que previene: _______________
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

if __name__ == '__main__':
    app.run(debug=False, port=5004)
```

Crea también el archivo `.env` con el siguiente contenido (genera un valor real):

```
SECRET_KEY=tu_clave_generada_aqui
```

Para generar la clave ejecuta en Python:

```python
import secrets
print(secrets.token_hex(32))
```

---

### Tarea 2.1 (30 pts) — Completar los 13 TODOs

Completa cada TODO en `app_segura.py`. **Para cada uno** agrega un comentario que responda:
1. ¿Qué vulnerabilidad específica previene este control?
2. ¿Por qué es necesario en el contexto de una tienda online?

Los 13 TODOs son:

| # | Ubicación | Qué implementar |
|---|---|---|
| 1 | `app.secret_key` | Leer de variable de entorno o generar aleatoriamente |
| 2 | Configuración Flask | Las 3 propiedades de cookie segura |
| 3 | `requiere_rol()` | Verificar autenticación (401 si no hay sesión) |
| 4 | `requiere_rol()` | Verificar que el rol esté en los permitidos (403 si no) |
| 5 | `login()` | Validación de username con regex |
| 6 | `login()` | Consulta parametrizada con `?` |
| 7 | `login()` | Verificación de contraseña con bcrypt |
| 8 | `login()` | Limpiar y regenerar sesión correctamente |
| 9 | `comprar()` | Validar CSRF token |
| 10 | `comprar()` | Validar monto (float, positivo, > 0) |
| 11 | `comprar()` | Consultas UPDATE e INSERT parametrizadas |
| 12 | `listar_pedidos()` | Decorador `@requiere_rol('admin')` |
| 13 | `headers_seguridad()` | Header Content-Security-Policy |

---

### Tarea 2.2 (10 pts) — Pruebas de seguridad

Crea `pruebas_seguridad.md` con evidencia de que tu implementación **rechaza los 3 ataques**:

**Prueba 1 — CSRF rechazado:**
- Levanta `app_segura.py` en puerto 5004
- Modifica `ataque_csrf.html` para apuntar a `http://localhost:5004/comprar`
- Abre el HTML en el navegador o usa curl
- Documenta la respuesta del servidor (debe ser HTTP 403)
- Explica en 2-3 oraciones por qué el ataque ya no funciona

**Prueba 2 — Contraseña MD5 crackeada rechazada:**
- Intenta hacer login en `app_segura.py` con las contraseñas que encontraste en CrackStation
- El usuario admin tenía contraseña "admin" en `app_vulnerable.py`
- Intenta `admin/admin` en `app_segura.py`
- Documenta la respuesta (debe ser HTTP 401)
- Explica por qué bcrypt no acepta la misma contraseña que MD5 verificaba

**Prueba 3 — Acceso denegado a panel admin:**
- Haz login como maria (rol: cliente)
- Intenta acceder a `GET /admin/pedidos`
- Documenta la respuesta (debe ser HTTP 403 con "Acceso denegado")
- Explica la diferencia entre HTTP 401 y HTTP 403

Formato sugerido para cada prueba:
```
## Prueba 1: CSRF rechazado
Comando curl utilizado: [...]
Respuesta del servidor: [...]
Análisis: [...]
```

---

### Tarea 2.3 (10 pts) — Reflexión final

Escribe una reflexión de **mínimo 150 palabras** respondiendo:

¿Por qué un sistema de pagos como TiendaApp necesita las 3 protecciones (CSRF + bcrypt + RBAC) **simultáneamente**? ¿Qué pasaría si solo implementas 2 de las 3?

Tu reflexión debe incluir un escenario de ataque concreto para **cada combinación de 2 protecciones sin la tercera**:

- Escenario A: tienes CSRF + bcrypt, pero **sin RBAC** → ¿qué puede hacer un atacante?
- Escenario B: tienes CSRF + RBAC, pero **sin bcrypt** → ¿qué puede hacer un atacante?
- Escenario C: tienes bcrypt + RBAC, pero **sin CSRF** → ¿qué puede hacer un atacante?

Concluye con una oración sobre el concepto de **defensa en profundidad** aplicado a este caso.

---

## PARTE 3 — DESAFÍO (30 min, 25 pts)

### Tarea 3.1 (15 pts) — Double Submit Cookie

Implementa el patrón **Double Submit Cookie** como alternativa al CSRF token en sesión.

**Concepto:**
- El servidor genera un token aleatorio y lo envía en **dos lugares**: una cookie Y en el body del formulario
- Al recibir el POST, el servidor verifica que el token de la cookie coincida con el del body
- Si no coinciden → rechazar (posible CSRF)
- Ventaja: no requiere almacenar estado en la sesión del servidor (útil para APIs stateless)

**Esqueleto a completar:**

```python
from flask import Flask, request, session, jsonify, make_response
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route('/obtener-token-ds')
def obtener_token():
    """
    Genera el token y lo envía tanto en cookie como en el body.
    El cliente debe guardar el valor del body y enviarlo en futuros POSTs.
    """
    token = secrets.token_hex(32)
    response = make_response(jsonify({"csrf_ds_token": token}))
    # Enviar el token en una cookie (HttpOnly=False para que JS pueda leerla)
    response.set_cookie(
        'csrf_ds_token',
        token,
        httponly=False,   # El JS del cliente necesita leer esta cookie
        secure=True,
        samesite='Strict'
    )
    return response

@app.route('/comprar-v2', methods=['POST'])
def comprar_v2():
    # El token viene en la cookie Y en el body del formulario
    token_cookie = request.cookies.get('csrf_ds_token')
    token_body = request.form.get('csrf_token')
    
    # TODO: Implementar la verificación del Double Submit Cookie
    # Considera los siguientes casos:
    # 1. ¿Qué pasa si token_cookie es None? (usuario no llamó a /obtener-token-ds)
    # 2. ¿Qué pasa si token_body es None? (formulario no incluye el token)
    # 3. ¿Cómo comparar los tokens de forma segura contra timing attacks?
    #    Pista: usa secrets.compare_digest() en vez de ==
    pass
    
    # Si los tokens son válidos, procesar la compra
    producto = request.form.get('producto', '')
    monto = request.form.get('monto', 0)
    return jsonify({"comprado": producto, "monto": monto})
```

**Preguntas a responder en comentarios del código:**
1. ¿Por qué el atacante no puede replicar este ataque aunque sepa el nombre de la cookie?
2. ¿Cuándo es el Double Submit Cookie **menos seguro** que el token en sesión?
   - Pista: investiga qué pasa si el atacante puede escribir cookies en subdominios del sitio víctima
3. ¿Por qué se usa `secrets.compare_digest()` en vez de `==` para comparar tokens?

---

### Tarea 3.2 (10 pts) — Investigación

Crea `investigacion.md` respondiendo las siguientes preguntas con detalle técnico:

**Pregunta 1 — Flask-WTF:**

¿Qué es Flask-WTF y cómo protege automáticamente contra CSRF con 3 líneas de código?

Tu respuesta debe incluir:
- Un ejemplo mínimo de código Flask-WTF con protección CSRF activada
- ¿Cómo genera y valida el token internamente?
- ¿Cuándo conviene usar Flask-WTF vs implementación manual como la de este lab?

**Pregunta 2 — Argon2 vs bcrypt:**

¿Cuál es la diferencia técnica entre Argon2 y bcrypt para almacenar contraseñas?

Tu respuesta debe incluir:
- ¿Qué parámetros tiene Argon2 que bcrypt no tiene? (pista: memoria RAM)
- ¿Cuál recomienda OWASP en su Password Storage Cheat Sheet de 2024?
- ¿Cómo migrarías las contraseñas bcrypt de esta app a Argon2 sin forzar a todos los usuarios a cambiar su contraseña?

**Pregunta 3 — flask-limiter:**

¿Qué es la librería `flask-limiter` y cómo previene ataques de fuerza bruta en el endpoint `/login`?

Tu respuesta debe incluir:
- Un ejemplo mínimo de código que limite el login a 5 intentos por IP por minuto
- ¿Qué respuesta HTTP devuelve cuando se excede el límite? (código y mensaje)
- ¿Qué backends de almacenamiento soporta flask-limiter? (memory, Redis, etc.)
- ¿Por qué limitar por IP no es suficiente en todos los casos?

---

## ENTREGABLES

Sube a GitHub en la carpeta `semana-07/lab-casa/`:

| Archivo | Descripción | Puntos |
|---|---|---|
| `app_vulnerable.py` | Código original con análisis en comentarios | — |
| `ataque_csrf.html` | Archivo del atacante con comentarios línea a línea | 10 pts |
| `app_segura.py` | 13 TODOs completados con comentarios explicativos | 30 pts |
| `.env` | Contiene SECRET_KEY generada (NO subir, ver .gitignore) | — |
| `.gitignore` | Debe excluir `.env` como mínimo | — |
| `pruebas_seguridad.md` | Evidencia documentada de los 3 ataques rechazados | 10 pts |
| `investigacion.md` | Respuestas a las 3 preguntas de Tarea 3.2 | 10 pts |

**Importante sobre el `.gitignore`:**
```
# .gitignore mínimo requerido
.env
__pycache__/
*.pyc
*.pyo
.DS_Store
```

---

## RUBRICA DE EVALUACION

| Criterio | Excelente (100%) | Suficiente (60%) | Insuficiente (<60%) | Puntaje |
|---|---|---|---|---|
| Tabla de vulnerabilidades (Tarea 1.1) | 5+ vulnerabilidades con línea exacta, OWASP correcto, impacto específico y forma de explotación | 3-4 vulnerabilidades con OWASP básico | Menos de 3 o sin categoría OWASP | 10 pts |
| ataque_csrf.html (Tarea 1.2) | Funcional, comentado línea a línea, explicación completa de por qué funciona sin clic | Funcional pero sin comentarios o sin explicación final | No funcional o incompleto | 10 pts |
| CrackStation + reflexión MD5 (Tarea 1.3) | Contraseñas encontradas, tiempo documentado, análisis de implicaciones con datos (intentos/segundo) | Solo contraseñas sin reflexión técnica | Incompleto o sin evidencia | 5 pts |
| 13 TODOs con comentarios (Tarea 2.1) | Todos correctos, cada uno con comentario técnico de vulnerabilidad prevenida y razón | 8-12 correctos con algunos comentarios | Menos de 8 correctos | 30 pts |
| Pruebas de rechazo (Tarea 2.2) | 3 pruebas documentadas con output real + explicación técnica de por qué cada una falla | 2 pruebas sin explicación detallada | Menos de 2 pruebas | 10 pts |
| Reflexión final (Tarea 2.3) | 3 escenarios de ataque concretos, argumentación coherente, mínimo 150 palabras, menciona defensa en profundidad | Solo menciona las 3 protecciones sin escenarios | Superficial o menos de 100 palabras | 10 pts |
| Double Submit Cookie (Tarea 3.1) | Implementado correctamente con `secrets.compare_digest()`, explica cuándo es menos seguro y por qué | Implementado pero sin análisis de debilidades o sin `compare_digest` | No implementado | 15 pts |
| Investigación Flask-WTF/Argon2/flask-limiter (Tarea 3.2) | Comparación técnica con código de ejemplo en las 3 preguntas | Solo descripción sin código en al menos 2 preguntas | Incompleto o sin código | 10 pts |
| **TOTAL** | | | | **100 pts** |

---

## FECHA DE ENTREGA

- Subir al repositorio GitHub antes del inicio de la Semana 8
- El link del repositorio se entrega por el campus virtual
- Se evalúa el último commit antes de la hora límite
- Commits después de la fecha límite no serán considerados

---

*Programación Segura DD281 — Universidad Autónoma del Perú — Semana 7*
