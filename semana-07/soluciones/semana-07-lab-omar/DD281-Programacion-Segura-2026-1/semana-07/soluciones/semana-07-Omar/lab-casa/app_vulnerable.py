"""
app_vulnerable.py — TiendaApp con vulnerabilidades intencionales
Programación Segura DD281 — Semana 7
ANÁLISIS DE VULNERABILIDADES (ver Tarea 1.1 en README o tabla de entrega)
"""

from flask import Flask, request, session, jsonify, redirect
import sqlite3, hashlib, os

app = Flask(__name__)

# VULNERABILIDAD 1 (Línea 12): Clave secreta hardcodeada y débil
# OWASP A02 - Cryptographic Failures / A05 - Security Misconfiguration
# Riesgo: ALTO — cualquier atacante que lea el código puede forjar cookies de sesión
app.secret_key = "tienda2024"

# VULNERABILIDAD 2 (Configuración de cookies): Sin SameSite, sin HttpOnly, sin Secure
# OWASP A05 - Security Misconfiguration
# Riesgo: ALTO — cookies accesibles por JavaScript (XSS) y enviadas en peticiones cross-site (CSRF)
# Sin SameSite ni HttpOnly


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
        -- VULNERABILIDAD 3 (datos): Contraseñas MD5 sin salt
        -- OWASP A02 - Cryptographic Failures
        -- Riesgo: CRÍTICO — MD5 es un algoritmo de hashing rápido, no diseñado para contraseñas;
        --         se crackea en segundos con tablas rainbow o GPU modernas (>10,000 millones hash/seg)
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

    # VULNERABILIDAD 4 (Línea 62): MD5 para contraseñas
    # OWASP A02 - Cryptographic Failures
    # Riesgo: CRÍTICO — MD5 no tiene salt, es reversible via tablas rainbow y muy rápido para fuerza bruta
    password_md5 = hashlib.md5(password.encode()).hexdigest()

    conn = get_db()

    # VULNERABILIDAD 5 (Línea 65-67): SQL Injection con f-string
    # OWASP A03 - Injection
    # Riesgo: CRÍTICO — Un atacante puede escribir ' OR '1'='1'-- en username y saltarse la autenticación
    # Explotación: username = "' OR '1'='1'--" omite la verificación de contraseña completamente
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

    # VULNERABILIDAD 6 (Línea 82): Sin CSRF token
    # OWASP A01 - Broken Access Control (CSRF)
    # Riesgo: ALTO — Cualquier sitio externo puede forzar al usuario autenticado a realizar compras
    # El navegador envía automáticamente las cookies de sesión en peticiones cross-origin POST
    producto = request.form.get('producto')
    monto = float(request.form.get('monto', 0))

    conn = get_db()

    # VULNERABILIDAD 7 (Línea 87-93): SQL Injection en UPDATE e INSERT con f-strings
    # OWASP A03 - Injection
    # Riesgo: ALTO — El campo 'producto' no está sanitizado, podría manipular la consulta SQL
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
    # VULNERABILIDAD 8 (Línea 98-103): Sin verificación de rol (Broken Access Control)
    # OWASP A01 - Broken Access Control
    # Riesgo: ALTO — Cualquier usuario autenticado (incluso 'cliente') puede ver todos los pedidos
    # Explotación: hacer login como maria (cliente) y acceder a GET /admin/pedidos
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
