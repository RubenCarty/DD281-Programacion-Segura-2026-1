# LABORATORIO EN CLASE — SEMANA 7
## Programación Segura DD281 | Universidad Autónoma del Perú
**Tema:** CSRF, Contraseñas Seguras y Controles de Acceso
**Tiempo:** 35 minutos
**Modalidad:** Individual
**Plataforma:** Replit (replit.com) o VS Code + Python
**Puntaje:** 20 puntos (evaluación formativa)

---

## ACCESO EN 2 MINUTOS

**Opción A — Replit (sin instalación):**
1. Ir a replit.com → Create Repl → Python → nombrar "S7-CSRF-Lab" → Run
2. En la consola de Replit ejecutar: `pip install flask bcrypt`
3. Crear el archivo `app_vulnerable.py` con el código del escenario
4. Ejecutar con el botón Run

**Opción B — VS Code local:**
1. Tener Python 3.10+ instalado
2. Ejecutar en terminal: `pip install flask bcrypt`
3. Crear el archivo y ejecutar: `python app_vulnerable.py`

---

## ESCENARIO

**"SeguridadPeru.pe — Endpoint vulnerable en producción"**

El equipo de desarrollo de SeguridadPeru.pe dejó este código en producción. Tu rol hoy es el de un **auditor de seguridad** que tiene 35 minutos para:
1. Identificar las vulnerabilidades críticas (Ejercicio 1)
2. Corregir el código (Ejercicio 2)
3. Reflexionar sobre cuál es el riesgo más grave (Ejercicio 3)

**Código en producción — `app_vulnerable.py`:**

```python
from flask import Flask, request, session, jsonify
import sqlite3, hashlib

app = Flask(__name__)
app.secret_key = "sp2024"

def get_db():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    conn.executescript('''
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY,
            user TEXT,
            pass_hash TEXT,
            rol TEXT,
            creditos REAL
        );
        INSERT INTO usuarios VALUES (1, 'admin', '21232f297a57a5a743894a0e4a801fc3', 'admin', 9999.0);
        INSERT INTO usuarios VALUES (2, 'cliente1', '827ccb0eea8a706c4c34a16891f84e7b', 'cliente', 100.0);
    ''')
    return conn

@app.route('/login', methods=['POST'])
def login():
    u = request.form.get('u')
    p = hashlib.md5(request.form.get('p', '').encode()).hexdigest()
    conn = get_db()
    user = conn.execute(f"SELECT * FROM usuarios WHERE user='{u}' AND pass_hash='{p}'").fetchone()
    conn.close()
    if user:
        session['id'] = user['id']
        session['rol'] = user['rol']
        return jsonify({"ok": True, "rol": user['rol']})
    return jsonify({"error": "fail"}), 401

@app.route('/transferir-creditos', methods=['POST'])
def transferir():
    if not session.get('id'):
        return jsonify({"error": "auth"}), 401
    monto = request.form.get('monto')
    destino = request.form.get('destino')
    conn = get_db()
    conn.execute(f"UPDATE usuarios SET creditos=creditos-{monto} WHERE id={session['id']}")
    conn.execute(f"UPDATE usuarios SET creditos=creditos+{monto} WHERE user='{destino}'")
    conn.commit()
    return jsonify({"ok": True})

@app.route('/panel-admin')
def panel_admin():
    conn = get_db()
    data = conn.execute("SELECT id, user, rol, creditos FROM usuarios").fetchall()
    conn.close()
    return jsonify([dict(r) for r in data])

if __name__ == '__main__':
    app.run(debug=True, port=5005)
```

---

## EJERCICIO 1 — Tabla de auditoría (10 min, 8 pts)

Lee el código cuidadosamente e identifica las vulnerabilidades. Completa la siguiente tabla en tu archivo `auditoria.md`:

| # | Función/Línea | Vulnerabilidad | OWASP 2021 | Impacto si se explota |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |

**Categorías OWASP 2021 de referencia para este ejercicio:**
- A01:2021 Broken Access Control
- A02:2021 Cryptographic Failures
- A03:2021 Injection

**Preguntas de andamiaje** (úsalas si te bloqueas):
- ¿Qué pasa si escribes `' OR '1'='1'--` en el campo "user" del formulario de login?
- ¿Qué pasa si cambias el valor de `monto` por un número negativo en `/transferir-creditos`?
- ¿Puede un usuario con rol "cliente" acceder a `/panel-admin`?
- ¿Cuánto tiempo tarda CrackStation en revertir un hash MD5 simple?

**Criterio de evaluación Ejercicio 1:**
- 8 pts: 4 vulnerabilidades correctas con OWASP y descripción de impacto específico
- 5 pts: 3 vulnerabilidades correctas
- 3 pts: 2 vulnerabilidades correctas
- 0 pts: menos de 2

---

## EJERCICIO 2 — Corrección del código (20 min, 8 pts)

Reescribe las funciones vulnerables de forma segura. Crea el archivo `app_corregida.py` con las siguientes correcciones obligatorias:

### Función `login()` — requisitos mínimos:

```python
@app.route('/login', methods=['POST'])
def login():
    u = request.form.get('u', '').strip()
    p = request.form.get('p', '')
    
    # CORREGIR 1: Usar consulta parametrizada con "?" (no f-string con 'u')
    # CORREGIR 2: Verificar contraseña con bcrypt.checkpw() (no MD5)
    # CORREGIR 3: Ejecutar session.clear() ANTES de guardar datos del usuario
    # CORREGIR 4: Generar csrf_token y guardarlo en session
    
    # Tu código aquí...
    pass
```

### Función `transferir()` — requisitos mínimos:

```python
@app.route('/transferir-creditos', methods=['POST'])
def transferir():
    if not session.get('id'):
        return jsonify({"error": "auth"}), 401
    
    # CORREGIR 5: Validar CSRF token (comparar request.form['csrf_token'] con session['csrf_token'])
    # CORREGIR 6: Validar que monto sea positivo (float > 0)
    # CORREGIR 7: Usar consultas parametrizadas para los dos UPDATE (no f-strings)
    
    # Tu código aquí...
    pass
```

### Función `panel_admin()` — requisitos mínimos:

```python
# CORREGIR 8: Agregar decorador @requiere_rol('admin') antes de la función
# Para eso necesitas implementar el decorador requiere_rol primero
@app.route('/panel-admin')
def panel_admin():
    conn = get_db()
    data = conn.execute("SELECT id, user, rol, creditos FROM usuarios").fetchall()
    conn.close()
    return jsonify([dict(r) for r in data])
```

**Imports adicionales necesarios:**

```python
import bcrypt, secrets
from functools import wraps
```

**Criterio de evaluación Ejercicio 2:**
- 8 pts: Las 3 funciones corregidas con todos los requisitos cumplidos
- 5 pts: 2 funciones correctas o 3 funciones con algunos requisitos faltantes
- 3 pts: Solo login() corregido correctamente
- 0 pts: Sin correcciones funcionales

---

## EJERCICIO 3 — Reflexión (5 min, 4 pts)

En **2-3 oraciones**, responde la siguiente pregunta en tu archivo `auditoria.md`:

**¿Cuál de las 3 vulnerabilidades del código (CSRF, hash MD5, falta de RBAC) es la más peligrosa para una aplicación de créditos como SeguridadPeru.pe y por qué?**

Guía para tu argumentación:
- Considera qué impacto financiero directo puede tener cada vulnerabilidad
- ¿Cuál de las 3 puede ser explotada sin necesitar las credenciales del usuario?
- ¿Cuál permite a un atacante actuar como si fuera un usuario legítimo sin que este lo sepa?

**Criterio de evaluación Ejercicio 3:**
- 4 pts: Elige una vulnerabilidad, justifica con impacto concreto en créditos/dinero, menciona por qué las otras 2 son menos graves en este contexto específico
- 2 pts: Elige una vulnerabilidad con justificación parcial
- 0 pts: No responde o responde sin argumentación

---

## ENTREGABLE

Al finalizar la sesión, muestra al docente los archivos:

1. `auditoria.md` — con la tabla de Ejercicio 1 y la reflexión de Ejercicio 3
2. `app_corregida.py` — con las 3 funciones corregidas

**El docente verificará:**
- Que el login usa `?` como placeholder (no f-string)
- Que `transferir()` valida el csrf_token antes de ejecutar los UPDATE
- Que `panel_admin()` rechaza con 403 a usuarios con rol "cliente"

---

## ROL DEL DOCENTE

**Durante el Ejercicio 1 (primeros 10 min):**
- Circular y verificar que los estudiantes identifican al menos 3 vulnerabilidades
- Para quien se bloquea, usar esta pregunta de andamiaje: *"¿Qué pasa si cambias el `monto` en `/transferir-creditos` por un número negativo?"*
- Señal de comprensión temprana: el estudiante señala TANTO la f-string en login() COMO la ausencia de CSRF token en transferir()

**Durante el Ejercicio 2 (siguientes 20 min):**
- Verificar que el estudiante usa `?` en lugar de f-string — esta es la corrección mínima aceptable
- Pregunta de andamiaje para bcrypt: *"¿Cómo sabe bcrypt si la contraseña ingresada coincide con el hash almacenado, si bcrypt es diferente a MD5?"*
- Error frecuente a vigilar: `conn.execute("SELECT... WHERE user=?", username)` sin la coma → debe ser `(username,)` con coma al final

**Durante el Ejercicio 3 (últimos 5 min):**
- Pedir a **2 estudiantes** que lean en voz alta su corrección de `transferir()` — discutir diferencias de implementación con el grupo
- Pregunta de cierre para el grupo: *"Si solo pueden implementar UNA de las 3 correcciones por falta de tiempo, ¿cuál priorizan y por qué?"*

**Señales de comprensión para el cierre:**
- El estudiante verbaliza: "sin CSRF token, cualquier página web puede hacer transferencias en mi nombre"
- El estudiante distingue entre HTTP 401 (no autenticado) y HTTP 403 (autenticado pero sin permiso)
- El estudiante entiende que MD5 no es un hash de contraseñas sino un hash de integridad

---

## REFERENCIA RAPIDA — SINTAXIS CLAVE

Para quienes necesitan recordatorio rápido de la sintaxis:

**Consulta parametrizada (correcto):**
```python
user = conn.execute(
    "SELECT * FROM usuarios WHERE user=?",
    (u,)   # <- la coma es obligatoria para crear una tupla
).fetchone()
```

**bcrypt — verificar contraseña:**
```python
import bcrypt
if bcrypt.checkpw(p.encode('utf-8'), user['pass_hash'].encode('utf-8')):
    # contraseña correcta
```

**CSRF token — generar y validar:**
```python
import secrets

# Al hacer login (guardar en sesión):
session['csrf_token'] = secrets.token_hex(32)

# Al recibir POST (validar):
token = request.form.get('csrf_token')
if not token or token != session.get('csrf_token'):
    return jsonify({"error": "CSRF inválido"}), 403
```

**Decorador requiere_rol:**
```python
from functools import wraps

def requiere_rol(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get('id'):
                return jsonify({"error": "No autenticado"}), 401
            if session.get('rol') not in roles:
                return jsonify({"error": "Acceso denegado"}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

# Uso:
@app.route('/panel-admin')
@requiere_rol('admin')
def panel_admin():
    ...
```

---

*Programación Segura DD281 — Universidad Autónoma del Perú — Semana 7*
