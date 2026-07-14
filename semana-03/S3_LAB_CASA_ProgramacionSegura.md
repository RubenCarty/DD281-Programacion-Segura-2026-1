# S3 — LABORATORIO EN CASA
## Sistema de Sesiones Seguras con RBAC en Flask

| Campo | Detalle |
|---|---|
| **Curso** | Programación Segura (DD281) — Semana 3 |
| **Nombre del estudiante** | _________________________________ |
| **Código** | _____________ |
| **Fecha de entrega** | _____________ |
| **Tiempo estimado** | 2 horas |
| **Modalidad** | Individual o en pareja |

---

## Objetivo

Implementar un sistema Flask con gestión de sesiones seguras, RBAC (3 roles), prevención de Session Fixation, y logout completo. Al finalizar, el estudiante tendrá un sistema funcional que aplica todas las buenas prácticas de sesiones de la semana 3.

**Competencia que desarrolla:** Modela un proyecto aplicando buenas prácticas en gestión de sesiones y seguridad basada en roles (Resultado de Aprendizaje S3).

---

## Software y Herramientas Requeridas

| Herramienta | Versión | Link de descarga |
|---|---|---|
| Python | 3.10 o superior | https://www.python.org/downloads/ |
| Flask | 3.0.x | `pip install flask` |
| Visual Studio Code | Última | https://code.visualstudio.com/ |
| Navegador con DevTools | Chrome / Firefox | Ya instalado |

**Verificación de entorno (ejecutar en terminal):**
```bash
python --version          # Debe mostrar Python 3.10+
pip install flask
python -c "import flask; print(flask.__version__)"  # Debe mostrar 3.x.x
```

**Alternativa online (sin instalación):** https://replit.com — crear proyecto Python, pegar el código.

---

## Estructura del Proyecto a Crear

```
lab_s3_sesiones/
├── app.py              ← Aplicación principal (tú lo completas)
├── templates/
│   ├── login.html      ← Formulario de login
│   ├── dashboard.html  ← Panel según rol
│   ├── admin.html      ← Solo admin
│   └── error.html      ← Error 403 / 401
└── requirements.txt    ← flask
```

---

## PARTE 1 — EXPLORACIÓN (30 min)

### Objetivo: Entender cómo Flask maneja sesiones y observar cookies en DevTools

**Paso 1.1 — Crear el proyecto base**

```bash
mkdir lab_s3_sesiones
cd lab_s3_sesiones
mkdir templates
```

**Paso 1.2 — Instalar dependencias**
```bash
pip install flask
echo "flask==3.0.3" > requirements.txt
```

**Paso 1.3 — Crear app.py con la exploración inicial**

```python
# app.py — PARTE 1: Exploración de sesiones en Flask
from flask import Flask, session, redirect, url_for, request, make_response
import os, secrets

app = Flask(__name__)

# ─── CONFIGURACIÓN DE SEGURIDAD DE SESIONES ───────────────────────────────
# Completa los valores correctos según lo aprendido en clase:
app.config['SECRET_KEY'] = secrets.token_hex(32)

# TODO 1: Completar la configuración de seguridad de cookies
app.config.update(
    SESSION_COOKIE_HTTPONLY = True,      # Completa: True o False?
    SESSION_COOKIE_SECURE   = False,     # False en desarrollo local (True en producción)
    SESSION_COOKIE_SAMESITE = 'Lax',    # Completa: 'Strict', 'Lax', o 'None'?
)

# ─── USUARIOS DE PRUEBA (en producción: usar BD con bcrypt) ───────────────
USUARIOS = {
    'admin@test.com':      {'password': 'Admin2026!',   'role': 'admin',      'nombre': 'Ana Admin'},
    'supervisor@test.com': {'password': 'Super2026!',   'role': 'supervisor', 'nombre': 'Pedro Sup'},
    'usuario@test.com':    {'password': 'Usuario2026!', 'role': 'usuario',    'nombre': 'María User'},
}

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        user = USUARIOS.get(email)
        if user and user['password'] == password:
            # TODO 2: Implementar prevención de Session Fixation aquí
            # Pista: ¿qué debes hacer ANTES de asignar datos del usuario?
            # _______________________________________________
            
            session['user_id']    = email
            session['user_role']  = user['role']
            session['user_name']  = user['nombre']
            session.permanent     = True
            
            return redirect(url_for('dashboard'))
        
        return render_template('login.html', error='Credenciales incorrectas')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html',
                           name=session['user_name'],
                           role=session['user_role'])

@app.route('/logout')
def logout():
    # TODO 3: Implementar logout correcto (servidor + cliente)
    # Recuerda: dos acciones necesarias
    # _______________________________________________
    pass

if __name__ == '__main__':
    from flask import render_template
    app.run(debug=True, port=5000)
```

**Paso 1.4 — Crear templates/login.html**

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Login Seguro — Lab S3</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; }
        input { width: 100%; padding: 8px; margin: 8px 0; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #2c3e50; color: white; border: none; cursor: pointer; }
        .error { color: red; }
    </style>
</head>
<body>
    <h2>Programación Segura — Lab S3</h2>
    <h3>Sistema con Sesiones Seguras y RBAC</h3>
    {% if error %}<p class="error">{{ error }}</p>{% endif %}
    <form method="POST">
        <input type="email"    name="email"    placeholder="Correo electrónico" required>
        <input type="password" name="password" placeholder="Contraseña" required>
        <button type="submit">Iniciar Sesión</button>
    </form>
    <br>
    <small>
        Usuarios de prueba:<br>
        admin@test.com / Admin2026!<br>
        supervisor@test.com / Super2026!<br>
        usuario@test.com / Usuario2026!
    </small>
</body>
</html>
```

**Paso 1.5 — Crear templates/dashboard.html**

```html
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><title>Dashboard</title>
<style>
    body { font-family: Arial; max-width: 600px; margin: 40px auto; }
    .badge { background: #2c3e50; color: white; padding: 4px 10px; border-radius: 12px; }
    .admin-badge { background: #c0392b; }
    .supervisor-badge { background: #e67e22; }
    a { color: #2c3e50; }
</style>
</head>
<body>
    <h2>Dashboard</h2>
    <p>Bienvenido, <strong>{{ name }}</strong> 
       <span class="badge {{ role }}-badge">{{ role | upper }}</span>
    </p>
    <hr>
    <ul>
        <li><a href="/mi-perfil">Mi Perfil</a></li>
        <li><a href="/reportes">Ver Reportes</a> (supervisor y admin)</li>
        <li><a href="/admin/panel">Panel de Administración</a> (solo admin)</li>
    </ul>
    <br>
    <a href="/logout">Cerrar Sesión</a>
</body>
</html>
```

**Paso 1.6 — Ejecutar y observar**
```bash
python app.py
```
Navega a `http://localhost:5000` → haz login → abre DevTools (F12) → Application → Cookies.

---

**Preguntas de reflexión Parte 1:**

**P1.1:** ¿Qué valor tiene la cookie `session` que aparece en DevTools? ¿Es el email del usuario directamente?

*Tu respuesta:* ___________________________________________________

**P1.2:** ¿Qué pasa si cambias el atributo `SESSION_COOKIE_HTTPONLY` a `False`? Observa qué cambia en DevTools.

*Tu respuesta:* ___________________________________________________

**P1.3:** Abre la consola de DevTools y ejecuta `document.cookie`. ¿Qué muestra? ¿Por qué?

*Tu respuesta:* ___________________________________________________

---

## PARTE 2 — APLICACIÓN (60 min)

### Objetivo: Implementar RBAC completo con 3 roles y prevención de ataques

**Paso 2.1 — Completar los TODO del app.py**

Vuelve a `app.py` y completa los tres TODO:

**TODO 2 — Session Fixation:** Agrega la línea que previene Session Fixation después de validar credenciales.

**TODO 3 — Logout correcto:** Implementa el logout en dos pasos (servidor + cliente).

---

**Paso 2.2 — Agregar el decorador RBAC y las rutas protegidas**

Agrega este código a `app.py` DESPUÉS de la configuración inicial:

```python
from functools import wraps
from flask import abort, render_template
from datetime import timedelta

# ─── CONFIGURACIÓN DE TIMEOUT ────────────────────────────────────────────────
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# ─── DECORADOR RBAC ──────────────────────────────────────────────────────────
def require_role(*roles):
    """
    Verifica que el usuario tenga el rol correcto.
    El rol se lee del SERVIDOR (session), nunca del cliente.
    """
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            # Paso 1: ¿está autenticado?
            if 'user_id' not in session:
                return redirect(url_for('login'))
            # Paso 2: ¿tiene el rol necesario?
            if session.get('user_role') not in roles:
                return render_template('error.html', 
                                       code=403,
                                       msg=f"Acceso denegado. Requiere: {roles}"), 403
            return f(*args, **kwargs)
        return inner
    return decorator

# ─── RUTAS PROTEGIDAS POR ROL ────────────────────────────────────────────────
@app.route('/mi-perfil')
@require_role('admin', 'supervisor', 'usuario')   # Cualquier usuario autenticado
def mi_perfil():
    return render_template('dashboard.html',
                           name=session['user_name'],
                           role=session['user_role'],
                           seccion="Mi Perfil")

@app.route('/reportes')
@require_role('admin', 'supervisor')             # Solo admin o supervisor
def ver_reportes():
    reportes = [
        {'titulo': 'Reporte de Accesos',    'fecha': '2026-06-15'},
        {'titulo': 'Reporte de Sesiones',   'fecha': '2026-06-14'},
        {'titulo': 'Reporte de Incidentes', 'fecha': '2026-06-13'},
    ]
    return render_template('dashboard.html',
                           name=session['user_name'],
                           role=session['user_role'],
                           seccion="Reportes",
                           reportes=reportes)

@app.route('/admin/panel')
@require_role('admin')                           # SOLO admin
def panel_admin():
    # TODO 4: Completar esta función para mostrar la lista de USUARIOS
    # (la lista USUARIOS está definida arriba del app.py)
    # Tu código aquí:
    pass

@app.route('/admin/usuarios/<email>/eliminar', methods=['POST'])
@require_role('admin')
def eliminar_usuario(email):
    # TODO 5: Implementar eliminación con validación:
    # 1. El admin no puede eliminarse a sí mismo
    # 2. Si el email no existe, retornar 404
    # Tu código aquí:
    pass
```

---

**Paso 2.3 — Crear templates/error.html**

```html
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Error {{ code }}</title>
<style>body{font-family:Arial;text-align:center;margin-top:80px;}</style>
</head>
<body>
    <h1 style="color:#c0392b">Error {{ code }}</h1>
    <p>{{ msg }}</p>
    <a href="/dashboard">Volver al Dashboard</a> |
    <a href="/logout">Cerrar Sesión</a>
</body></html>
```

---

**Paso 2.4 — Probar el RBAC**

Realiza las siguientes pruebas y registra los resultados:

| Prueba | Usuario | Ruta | Resultado esperado | Resultado real |
|---|---|---|---|---|
| 1 | usuario@test.com | `/reportes` | 403 Acceso denegado | |
| 2 | supervisor@test.com | `/reportes` | 200 OK — muestra reportes | |
| 3 | usuario@test.com | `/admin/panel` | 403 Acceso denegado | |
| 4 | admin@test.com | `/admin/panel` | 200 OK — panel admin | |
| 5 | Sin login | `/dashboard` | Redirige a /login | |

**Pregunta 2.1:** ¿Qué pasaría si en la ruta `/admin/panel` verificaras el rol con `request.args.get('role') == 'admin'` en lugar del decorador? ¿Cómo lo explotaría un atacante?

*Tu respuesta:* ___________________________________________________
___________________________________________________

**Pregunta 2.2:** Después de hacer login como `usuario@test.com` e intentar `/admin/panel`, revisa la consola del navegador. ¿El error 403 revela información del servidor que no debería mostrarse?

*Tu respuesta:* ___________________________________________________

---

**Puntos de verificación Parte 2:**
- [ ] `session.clear()` en el login (previene Session Fixation)
- [ ] Logout limpia la sesión del servidor Y elimina la cookie del cliente
- [ ] `/reportes` retorna 403 para rol `usuario` y 200 para `supervisor`
- [ ] `/admin/panel` retorna 403 para todo rol que no sea `admin`
- [ ] La tabla de pruebas está completa con los resultados reales

---

## PARTE 3 — DESAFÍO (30 min)

### Objetivo: Agregar funcionalidades de seguridad avanzadas

**Desafío 3.1 — Simulación de Session Fixation**

Agrega esta ruta a tu `app.py` para demostrar el ataque y su prevención:

```python
@app.route('/demo/fixation')
def demo_fixation():
    """
    Ruta educativa que demuestra Session Fixation.
    Muestra el session_id antes y después del login.
    """
    # Obtener el session_id actual (antes del login)
    session_id_antes = request.cookies.get('session', 'Sin sesión previa')
    
    info = {
        'session_id_antes_login': session_id_antes[:20] + '...' if len(session_id_antes) > 20 else session_id_antes,
        'tiene_user_id': 'user_id' in session,
        'nota': 'Después del login, el session_id debería CAMBIAR completamente.'
    }
    
    return str(info)
```

Navega a `/demo/fixation` antes y después del login. ¿Cambia el session_id?

*Tu observación:* ___________________________________________________

---

**Desafío 3.2 — Auditoría de Sesiones Activas (investigación)**

Agrega un diccionario global que registre las sesiones activas (usuario, IP, hora de login, último acceso):

```python
# Agregar al app.py después de USUARIOS
import time
from datetime import datetime

sesiones_auditoria = {}  # {session_id_hash: {usuario, ip, login_at, last_seen}}

# Modificar la ruta /login para registrar en el diccionario de auditoría
# Modificar el decorador require_role para actualizar 'last_seen'
# Agregar ruta /admin/sesiones-activas que muestre el registro (solo admin)

# TODO 6: Implementar las tres modificaciones anteriores
```

---

**Pregunta de reflexión final:**

> "¿Cuál fue el concepto de esta sesión que encontraste más difícil de implementar? ¿Y cuál crees que tendrá mayor impacto en la seguridad de tu proyecto del curso? Justifica tu respuesta."

*Tu respuesta (mínimo 5 líneas):*

_____________________________________________________
_____________________________________________________
_____________________________________________________
_____________________________________________________
_____________________________________________________

---

## Entregables

Subir al aula virtual una **carpeta ZIP** llamada `Lab_S3_TuNombre_TuCodigo.zip` que contenga:

1. `app.py` — Código completo con los 5 TODO implementados
2. `templates/` — Todos los templates HTML
3. `requirements.txt`
4. `evidencias/` — Capturas de pantalla de:
   - DevTools mostrando la cookie segura con HttpOnly y SameSite
   - Las 5 pruebas de RBAC de la Parte 2 (tabla completa con screenshots)
   - DevTools antes y después del login (para Desafío 3.1)
5. `respuestas.md` — Un archivo Markdown con todas tus respuestas a las preguntas del laboratorio

---

## Rúbrica de Evaluación

| Criterio | Excelente (100%) | Suficiente (70%) | Insuficiente (<50%) |
|---|---|---|---|
| Cookie con atributos correctos (HttpOnly, SameSite, max_age) | Todos configurados y verificados en DevTools | Al menos 2 atributos correctos | Solo 1 o ninguno |
| Session Fixation prevenida (session.clear()) | Implementado y demostrado | Implementado pero no evidenciado | No implementado |
| RBAC funcional (3 roles, decorador correcto) | Los 3 roles, decorador lee de session del servidor | 2 de 3 roles funcionan | Rol leído del cliente |
| Logout correcto (servidor + cliente) | Ambos pasos implementados y verificados | Solo un paso | No implementado |
| Tabla de pruebas completa | 5/5 pruebas con resultado real | 3/5 pruebas | Menos de 3 |
| Reflexión final | Análisis profundo de 5+ líneas | Reflexión superficial de 3 líneas | Sin reflexión o copiada |

---

*Universidad Autónoma del Perú — DD281 Programación Segura — Semana 3 — 2026-1*
