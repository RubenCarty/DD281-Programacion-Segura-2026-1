from flask import Flask, request, session, jsonify, redirect, render_template
import sqlite3
import secrets
import bcrypt
import os
import logging
from functools import wraps
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# FIX V1+V2: Se lee la clave secreta desde variables de entorno
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Configuración de cookies de sesión seguras
app.config.update(
    SESSION_COOKIE_HTTPONLY  = True,
    SESSION_COOKIE_SAMESITE  = 'Strict',
    SESSION_COOKIE_SECURE    = False,   # True solo en producción con HTTPS
)

DB_FILE = "banco_segura.db"

# Decorador para implementar RBAC (Control de Acceso Basado en Roles)
def requiere_rol(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not session.get('user_id'):
                return jsonify({"error": "No autenticado"}), 401
            # FIX V5: El rol se valida desde los datos seguros de la sesión
            if session.get('rol') not in roles:
                return jsonify({"error": "Acceso denegado"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# --- FUNCIÓN DE PRUEBA (Definida antes de usarse) ---
def crear_usuario_prueba():
    import bcrypt
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    usuario = "admin3"
    clave = "password123"
    
    # Nota: Cambiado a 'password_hash' para que coincida con la columna que busca tu ruta /login
    clave_hash_bytes = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    try:
        # Se asume que tu tabla usa 'password_hash' y tiene columna 'rol'
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash, rol, saldo) VALUES (?, ?, ?, ?)", 
            (usuario, clave_hash_bytes, 'admin', 1000.0)
        )
        conn.commit()
        print("¡Usuario de prueba 'admin' creado con éxito!")
    except sqlite3.IntegrityError:
        print("El usuario 'admin' ya existe en la base de datos o la tabla difiere.")
    except sqlite3.OperationalError as e:
        print(f"Nota de Base de Datos: {e}")
    finally:
        conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    if not username or not password:
        return jsonify({"error": "Campos requeridos"}), 400

    conn = get_db()
    # FIX V4: Consulta parametrizada para evitar SQL Injection
    user = conn.execute("SELECT * FROM usuarios WHERE username=?", (username,)).fetchone()
    conn.close()

    # FIX V3: Verificación segura usando bcrypt
    if not user or not bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    # Prevención de Session Fixation
    session.clear()

    session['user_id']    = user['id']
    session['username']   = user['username']
    session['rol']        = user['rol']
    session['csrf_token'] = secrets.token_hex(32) # Token CSRF inicial

    return redirect('/dashboard')
@app.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return redirect('/login')
    return render_template('dashboard.html', username=session.get('username'), rol=session.get('rol'))
@app.route('/transferir', methods=['POST'])
def transferir():
    if not session.get('user_id'):
        return jsonify({"error": "No autenticado"}), 401

    # FIX V7: Validación robusta del token CSRF
    token_enviado  = request.form.get('csrf_token', '')
    token_sesion   = session.get('csrf_token', '')
    if not secrets.compare_digest(token_enviado, token_sesion):
        return jsonify({"error": "Token CSRF inválido"}), 403

    destino = request.form.get('destino', '').strip()
    try:
        # FIX V8: Validación de montos válidos y positivos
        monto = float(request.form.get('monto', '0'))
        if monto <= 0:
            return jsonify({"error": "El monto debe ser mayor a 0"}), 400
    except ValueError:
        return jsonify({"error": "Monto inválido"}), 400

    conn = get_db()
    remitente = conn.execute("SELECT saldo FROM usuarios WHERE id=?", (session['user_id'],)).fetchone()
    
    if not remitente or remitente['saldo'] < monto:
        conn.close()
        return jsonify({"error": "Saldo insuficiente"}), 400

    conn.execute("UPDATE usuarios SET saldo=saldo-? WHERE id=?", (monto, session['user_id']))
    conn.execute("UPDATE usuarios SET saldo=saldo+? WHERE username=?", (monto, destino))
    conn.commit()
    conn.close()

    # Regenerar el token tras un uso exitoso
    session['csrf_token'] = secrets.token_hex(32)
    return jsonify({"ok": True, "monto": monto, "a": destino})

@app.route('/admin/usuarios')
@requiere_rol('admin') # FIX V9: Ruta restringida exclusivamente a administradores
def listar_usuarios():
    conn = get_db()
    data = conn.execute("SELECT id, username, rol, saldo FROM usuarios").fetchall()
    conn.close()
    return jsonify([dict(r) for r in data])

# --- BLOQUE DE EJECUCIÓN AL FINAL ---
if __name__ == '__main__':
    crear_usuario_prueba()  # Ejecuta la creación justo antes de lanzar el servidor
    print("\n  Servidor SEGURO corriendo en http://localhost:5006\n")
    app.run(debug=False, port=5006)