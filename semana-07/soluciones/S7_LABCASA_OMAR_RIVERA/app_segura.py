"""
app_segura.py — TiendaApp con implementación segura
Programación Segura DD281 — Semana 7
Todos los TODOs completados con comentarios técnicos.
"""

from flask import Flask, request, session, jsonify, redirect, make_response
import sqlite3, bcrypt, secrets, os, re
from functools import wraps
from dotenv import load_dotenv

load_dotenv()  # Carga variables de .env

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# TODO 1: Leer SECRET_KEY de variable de entorno; si no existe, generar con secrets.token_hex(32)
# Vulnerabilidad que previene: Clave secreta débil o expuesta (OWASP A05 - Security Misconfiguration)
# Por qué es necesario: Una clave hardcodeada como "tienda2024" es visible para cualquiera que
#   acceda al código fuente. La SECRET_KEY se usa para firmar las cookies de sesión;
#   si un atacante la conoce, puede forjar cookies y suplantar a cualquier usuario.
#   Al leerla del entorno, nunca aparece en el código. Si no existe, se genera una
#   clave criptográficamente aleatoria de 32 bytes (256 bits) — imposible de adivinar.
# ─────────────────────────────────────────────────────────────────────────────
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

# ─────────────────────────────────────────────────────────────────────────────
# TODO 2: Configurar las 3 propiedades de seguridad de cookie de sesión
# Vulnerabilidad que previene: Robo de sesión via XSS y CSRF via cookies cross-site
#   (OWASP A02 - Cryptographic Failures, A07 - Identification and Authentication Failures)
# Por qué es necesario en una tienda online:
#   - SESSION_COOKIE_HTTPONLY=True → impide que JavaScript del navegador acceda a la cookie.
#     Sin esto, un script malicioso inyectado (XSS) puede robar la cookie y secuestrar la sesión.
#   - SESSION_COOKIE_SECURE=True  → solo envía la cookie por HTTPS, nunca HTTP plano.
#     Sin esto, un atacante en la misma red (MitM) puede interceptar la cookie.
#   - SESSION_COOKIE_SAMESITE='Strict' → el navegador NO envía la cookie en peticiones
#     que vienen de otros dominios (evil.com → localhost). Esto rompe la mayoría de ataques CSRF
#     incluso antes de validar el token.
# ─────────────────────────────────────────────────────────────────────────────
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'


def get_db():
    """Crea una base de datos en memoria con contraseñas bcrypt correctas."""
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row

    # bcrypt genera un salt único automáticamente; rounds=12 hace que cada hash
    # tarde ~250ms — lo suficientemente lento para que la fuerza bruta sea inviable.
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
    """Decorador que exige sesión activa; devuelve 401 si no hay user_id."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({"error": "No autenticado"}), 401
        return f(*args, **kwargs)
    return decorated


def requiere_rol(*roles):
    """Decorador de control de acceso basado en roles (RBAC)."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            # ─────────────────────────────────────────────────────────────────
            # TODO 3: Verificar autenticación (no user_id en session → 401)
            # Vulnerabilidad que previene: Acceso no autenticado a rutas protegidas
            #   (OWASP A01 - Broken Access Control)
            # Devolver 401 (Unauthorized) indica "necesitas autenticarte primero".
            # ─────────────────────────────────────────────────────────────────
            if not session.get('user_id'):
                return jsonify({"error": "No autenticado"}), 401

            # ─────────────────────────────────────────────────────────────────
            # TODO 4: Verificar que session['rol'] está en roles (si no → 403)
            # Vulnerabilidad que previene: Escalada de privilegios / Broken Access Control
            #   (OWASP A01 - Broken Access Control)
            # Un usuario autenticado con rol 'cliente' no debe acceder a rutas de 'admin'.
            # Devolver 403 (Forbidden) indica "te conozco, pero no tienes permiso".
            # IMPORTANTE: el rol se lee de la sesión del servidor, nunca del request del cliente.
            # ─────────────────────────────────────────────────────────────────
            if session.get('rol') not in roles:
                return jsonify({"error": "Acceso denegado"}), 403

            return f(*args, **kwargs)
        return decorated
    return decorator


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    # ─────────────────────────────────────────────────────────────────────────
    # TODO 5: Validar username con regex (solo letras, números, guiones bajos, guiones, 3-30 chars)
    # Vulnerabilidad que previene: SQL Injection y entrada de datos maliciosos
    #   (OWASP A03 - Injection)
    # Aunque el TODO 6 ya usa consultas parametrizadas, la validación de entrada
    # es una capa de defensa adicional (defensa en profundidad). Además, rechazar
    # usernames inválidos antes de consultar la base de datos reduce la carga y
    # evita registros de error innecesarios.
    # ─────────────────────────────────────────────────────────────────────────
    if not re.match(r'^[a-zA-Z0-9_-]{3,30}$', username):
        return jsonify({"error": "Username inválido"}), 400

    conn = get_db()

    # ─────────────────────────────────────────────────────────────────────────
    # TODO 6: Consulta parametrizada (no f-string con username)
    # Vulnerabilidad que previene: SQL Injection (OWASP A03 - Injection)
    # Con f-strings, un atacante puede escribir ' OR '1'='1'-- para saltarse
    # la autenticación. Con "?" como placeholder, el driver de sqlite3 trata
    # el valor como dato puro — nunca como parte del SQL — haciendo imposible
    # la inyección sin importar lo que escriba el usuario.
    # ─────────────────────────────────────────────────────────────────────────
    user = conn.execute(
        "SELECT * FROM usuarios WHERE username=?",
        (username,)
    ).fetchone()
    conn.close()

    if user:
        # ─────────────────────────────────────────────────────────────────────
        # TODO 7: Verificar contraseña con bcrypt.checkpw()
        # Vulnerabilidad que previene: Contraseñas débiles o crackeables
        #   (OWASP A02 - Cryptographic Failures)
        # bcrypt.checkpw() rehashea la contraseña ingresada con el salt único
        # almacenado en el hash y compara de forma segura. A diferencia de MD5
        # (que se crackea en segundos), bcrypt con rounds=12 tarda ~250ms por
        # intento, haciendo la fuerza bruta computacionalmente inviable.
        # ─────────────────────────────────────────────────────────────────────
        password_valida = bcrypt.checkpw(
            password.encode('utf-8'),
            user['password_hash'].encode('utf-8')
        )

        if not password_valida:
            return jsonify({"error": "Credenciales incorrectas"}), 401

        # ─────────────────────────────────────────────────────────────────────
        # TODO 8: Limpiar session y regenerar (session.clear() antes de guardar datos de usuario)
        # Vulnerabilidad que previene: Session Fixation
        #   (OWASP A07 - Identification and Authentication Failures)
        # Sin session.clear(), si un atacante logró inyectar un session ID conocido
        # antes del login, tras el login ese mismo ID queda autenticado y el atacante
        # puede usarlo. Al limpiar la sesión, se garantiza que el ID de sesión
        # post-login es completamente nuevo y desconocido para el atacante.
        # ─────────────────────────────────────────────────────────────────────
        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['rol'] = user['rol']

        # Generar CSRF token para esta sesión (64 caracteres hex aleatorios)
        session['csrf_token'] = secrets.token_hex(32)

        return jsonify({
            "mensaje": f"Bienvenido {user['username']}",
            "csrf_token": session['csrf_token']  # El cliente JS debe guardarlo y enviarlo en cada POST
        })

    return jsonify({"error": "Credenciales incorrectas"}), 401


@app.route('/comprar', methods=['POST'])
@requiere_login
def comprar():
    # ─────────────────────────────────────────────────────────────────────────
    # TODO 9: Validar CSRF token
    # Vulnerabilidad que previene: Cross-Site Request Forgery — CSRF
    #   (OWASP A01 - Broken Access Control)
    # El atacante puede forzar al navegador de la víctima a enviar un POST, pero
    # NO puede leer ni adivinar el csrf_token almacenado en la sesión del servidor,
    # porque eso requeriría acceso al servidor o a la cookie de sesión (protegida
    # por HttpOnly). Si el token no coincide, la petición se rechaza con 403.
    # ─────────────────────────────────────────────────────────────────────────
    token_recibido = request.form.get('csrf_token', '')
    token_sesion = session.get('csrf_token', '')

    if not token_recibido or not secrets.compare_digest(token_recibido, token_sesion):
        return jsonify({"error": "CSRF token inválido o ausente"}), 403

    # ─────────────────────────────────────────────────────────────────────────
    # TODO 10: Validar que monto sea float positivo y > 0
    # Vulnerabilidad que previene: Manipulación de parámetros / Business Logic Attack
    #   (OWASP A04 - Insecure Design)
    # Sin validación, un atacante podría enviar monto=0, monto=-100 (sumando saldo
    # en vez de restarlo) o monto=999999999 para llevar el saldo a negativo.
    # El try/except captura valores no numéricos; la condición > 0 garantiza que
    # solo se procesen transacciones con sentido económico.
    # ─────────────────────────────────────────────────────────────────────────
    try:
        monto = float(request.form.get('monto', 0))
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
    except (ValueError, TypeError):
        return jsonify({"error": "Monto inválido"}), 400

    producto = request.form.get('producto', '').strip()

    if not producto:
        return jsonify({"error": "Producto requerido"}), 400

    conn = get_db()

    # ─────────────────────────────────────────────────────────────────────────
    # TODO 11: Consultas parametrizadas para UPDATE e INSERT (no f-strings)
    # Vulnerabilidad que previene: SQL Injection (OWASP A03 - Injection)
    # Con f-strings, el campo 'producto' podría contener SQL malicioso (e.g.,
    # "', 0); DROP TABLE usuarios;--"). Con "?" como placeholder, sqlite3
    # escapa automáticamente el valor. IMPORTANTE: el user_id viene de la sesión
    # del servidor, nunca del request del cliente (previene IDOR — Insecure Direct
    # Object Reference), ya que un cliente malicioso podría enviar otro user_id.
    # ─────────────────────────────────────────────────────────────────────────
    conn.execute(
        "UPDATE usuarios SET saldo = saldo - ? WHERE id = ?",
        (monto, session['user_id'])
    )
    conn.execute(
        "INSERT INTO pedidos (usuario_id, producto, monto) VALUES (?, ?, ?)",
        (session['user_id'], producto, monto)
    )
    conn.commit()
    conn.close()

    # Regenerar CSRF token después de cada uso exitoso (previene ataques de replay)
    session['csrf_token'] = secrets.token_hex(32)

    return jsonify({
        "comprado": producto,
        "monto": monto,
        "csrf_token": session['csrf_token']  # Nuevo token para la próxima petición
    })


@app.route('/admin/pedidos')
# ─────────────────────────────────────────────────────────────────────────────
# TODO 12: Agregar decorador @requiere_rol('admin') aquí
# Vulnerabilidad que previene: Broken Access Control / falta de RBAC
#   (OWASP A01 - Broken Access Control)
# En app_vulnerable.py cualquier usuario autenticado (incluso 'cliente') puede
# acceder a este endpoint y ver todos los pedidos. Con @requiere_rol('admin'),
# el decorador verifica que session['rol'] == 'admin' antes de ejecutar la función.
# Un cliente que intente acceder recibirá HTTP 403 Forbidden.
# ─────────────────────────────────────────────────────────────────────────────
@requiere_rol('admin')
def listar_pedidos():
    conn = get_db()
    pedidos = conn.execute("SELECT * FROM pedidos").fetchall()
    conn.close()
    return jsonify([dict(p) for p in pedidos])


@app.route('/perfil')
@requiere_login
def perfil():
    conn = get_db()
    user = conn.execute(
        "SELECT id, username, saldo, rol FROM usuarios WHERE id=?",
        (session['user_id'],)
    ).fetchone()
    conn.close()
    return jsonify(dict(user))


@app.after_request
def headers_seguridad(response):
    # ─────────────────────────────────────────────────────────────────────────
    # TODO 13: Agregar Content-Security-Policy
    # Vulnerabilidad que previene: Cross-Site Scripting — XSS
    #   (OWASP A03 - Injection)
    # CSP le dice al navegador qué orígenes de scripts, estilos e imágenes son
    # legítimos. Con "default-src 'self'; script-src 'self'", el navegador solo
    # ejecuta scripts cargados desde el mismo dominio de la app. Un atacante que
    # logre inyectar <script src="https://evil.com/keylogger.js"> verá que el
    # navegador bloquea la carga por violar la política CSP.
    # ─────────────────────────────────────────────────────────────────────────
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"

    # X-Content-Type-Options: impide que el navegador "adivine" el tipo MIME de una respuesta
    # Previene: ataques de MIME sniffing donde un archivo subido como imagen
    # se ejecuta como JavaScript si el navegador cree que es un script.
    response.headers['X-Content-Type-Options'] = 'nosniff'

    # X-Frame-Options: impide que la app se cargue en un iframe desde otro dominio
    # Previene: Clickjacking — OWASP A04
    response.headers['X-Frame-Options'] = 'DENY'

    return response


if __name__ == '__main__':
    # debug=False en producción: evita exponer el debugger interactivo de Werkzeug
    # (que permite ejecutar código Python arbitrario en el servidor)
    app.run(debug=False, port=5004)
