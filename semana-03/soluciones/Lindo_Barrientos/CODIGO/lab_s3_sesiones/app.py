# ══════════════════════════════════════════════════════════════════
# app.py — Lab S3: Sistema de Sesiones Seguras con RBAC en Flask
# Programación Segura (DD281) — Semana 3
# Incluye los 6 TODO implementados (Partes 1, 2 y 3)
# ══════════════════════════════════════════════════════════════════
from flask import (Flask, session, redirect, url_for, request,
                   render_template, abort)
from functools import wraps
from datetime import timedelta, datetime
import secrets

app = Flask(__name__)

# Clave de firma de la cookie de sesión (alta entropía, CSPRNG)
app.config['SECRET_KEY'] = secrets.token_hex(32)

# ─── TODO 1: CONFIGURACIÓN DE SEGURIDAD DE COOKIES ────────────────────────────
app.config.update(
    SESSION_COOKIE_HTTPONLY = True,    # JS no puede leer la cookie -> mitiga robo por XSS
    SESSION_COOKIE_SECURE   = False,   # False en desarrollo local; True en producción (HTTPS)
    SESSION_COOKIE_SAMESITE = 'Lax',   # no se envía en POST cross-site -> mitiga CSRF
)

# Expiración de sesión (Parte 2)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# ─── USUARIOS DE PRUEBA (en producción: usar BD con bcrypt) ───────────────────
USUARIOS = {
    'admin@test.com':      {'password': 'Admin2026!',   'role': 'admin',      'nombre': 'Ana Admin'},
    'supervisor@test.com': {'password': 'Super2026!',   'role': 'supervisor', 'nombre': 'Pedro Sup'},
    'usuario@test.com':    {'password': 'Usuario2026!', 'role': 'usuario',    'nombre': 'María User'},
}

# ─── TODO 6: REGISTRO DE AUDITORÍA DE SESIONES ACTIVAS ────────────────────────
sesiones_auditoria = {}  # {email: {usuario, ip, login_at, last_seen}}


# ─── DECORADOR RBAC ───────────────────────────────────────────────────────────
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
                                       msg=f"Acceso denegado. Requiere uno de: {roles}"), 403
            # TODO 6: actualizar 'last_seen' del usuario en la auditoría
            email = session.get('user_id')
            if email in sesiones_auditoria:
                sesiones_auditoria[email]['last_seen'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return f(*args, **kwargs)
        return inner
    return decorator


# ─── RUTAS BÁSICAS ────────────────────────────────────────────────────────────
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
            # ─── TODO 2: PREVENCIÓN DE SESSION FIXATION ───────────────────────
            # Se limpia/regenera la sesión ANTES de asignar los datos del usuario,
            # para que cualquier session ID fijado por un atacante quede inservible.
            session.clear()

            session['user_id']   = email
            session['user_role'] = user['role']
            session['user_name'] = user['nombre']
            session.permanent    = True

            # TODO 6: registrar la sesión en la auditoría
            sesiones_auditoria[email] = {
                'usuario':  user['nombre'],
                'rol':      user['role'],
                'ip':       request.remote_addr,
                'login_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'last_seen':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }

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
    # ─── TODO 3: LOGOUT CORRECTO (servidor + cliente) ─────────────────────────
    # 1) Invalidar la sesión en el SERVIDOR (y quitarla de la auditoría)
    sesiones_auditoria.pop(session.get('user_id'), None)
    session.clear()
    # 2) Al limpiar la sesión, Flask reescribe/expira la cookie firmada del cliente
    return redirect(url_for('login'))


# ─── RUTAS PROTEGIDAS POR ROL ─────────────────────────────────────────────────
@app.route('/mi-perfil')
@require_role('admin', 'supervisor', 'usuario')   # cualquier usuario autenticado
def mi_perfil():
    return render_template('dashboard.html',
                           name=session['user_name'],
                           role=session['user_role'],
                           seccion="Mi Perfil")


@app.route('/reportes')
@require_role('admin', 'supervisor')              # solo admin o supervisor
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
@require_role('admin')                            # SOLO admin
def panel_admin():
    # ─── TODO 4: mostrar la lista de USUARIOS ─────────────────────────────────
    return render_template('admin.html',
                           name=session['user_name'],
                           role=session['user_role'],
                           usuarios=USUARIOS,
                           sesiones=sesiones_auditoria)


@app.route('/admin/usuarios/<email>/eliminar', methods=['POST'])
@require_role('admin')
def eliminar_usuario(email):
    # ─── TODO 5: eliminación con validaciones ─────────────────────────────────
    # 1. El admin no puede eliminarse a sí mismo
    if email == session.get('user_id'):
        return render_template('error.html', code=400,
                               msg="No puedes eliminar tu propia cuenta."), 400
    # 2. Si el email no existe, retornar 404
    if email not in USUARIOS:
        abort(404)
    del USUARIOS[email]
    sesiones_auditoria.pop(email, None)
    return redirect(url_for('panel_admin'))


# ─── PARTE 3 — DESAFÍOS ───────────────────────────────────────────────────────
@app.route('/demo/fixation')
def demo_fixation():
    """Ruta educativa que demuestra Session Fixation: muestra el session_id
    antes y después del login (debe CAMBIAR tras autenticarse)."""
    session_id_antes = request.cookies.get('session', 'Sin sesión previa')
    info = {
        'session_id_antes_login': (session_id_antes[:20] + '...'
                                   if len(session_id_antes) > 20 else session_id_antes),
        'tiene_user_id': 'user_id' in session,
        'nota': 'Después del login, el session_id debería CAMBIAR completamente.'
    }
    return str(info)


@app.route('/admin/sesiones-activas')
@require_role('admin')   # TODO 6: solo admin ve las sesiones activas
def sesiones_activas():
    filas = "".join(
        f"<tr><td>{e}</td><td>{d['usuario']}</td><td>{d['rol']}</td>"
        f"<td>{d['ip']}</td><td>{d['login_at']}</td><td>{d['last_seen']}</td></tr>"
        for e, d in sesiones_auditoria.items()
    )
    return (f"<h2>Sesiones activas</h2><table border='1' cellpadding='6'>"
            f"<tr><th>Email</th><th>Usuario</th><th>Rol</th><th>IP</th>"
            f"<th>Login</th><th>Último acceso</th></tr>{filas}</table>"
            f"<br><a href='/dashboard'>Volver</a>")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
