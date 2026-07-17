from flask import Flask, request, session, jsonify, redirect
import sqlite3
import hashlib
import logging

app = Flask(__name__)
app.secret_key = "banco2024"        # V1: clave débil y hardcodeada

# V2: Credenciales de producción hardcodeadas en el código
DB_PASS = "BancoAdmin2024"
DB_URL  = f"postgresql://admin:{DB_PASS}@prod-db.banco.pe:5432/clientes"

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
DB_FILE = "banco_vulnerable.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    # V3: MD5 — crackeado en <1 segundo
    password_hash = hashlib.md5(password.encode()).hexdigest()

    conn = get_db()
    # V4: SQL Injection — consulta concatenada con f-string
    query = f"SELECT * FROM usuarios WHERE username='{username}' AND password_hash='{password_hash}'"
    logging.debug(f"SQL ejecutado: {query}")
    user = conn.execute(query).fetchone()
    conn.close()

    if user:
        session['user_id']  = user['id']
        session['username'] = user['username']
        session['rol']      = 'cliente'     # V5: siempre 'cliente', nunca lee BD
        # V6: password en texto plano en logs
        logging.debug(f"Login exitoso: user={username} | password={password}")
        return jsonify({"ok": True})

    return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route('/transferir', methods=['POST'])
def transferir():
    if not session.get('user_id'):
        return jsonify({"error": "No autenticado"}), 401

    destino = request.form.get('destino', '')
    monto   = request.form.get('monto', '0')

    # V7: Sin CSRF token — cualquier página puede disparar esta transferencia
    # V8: Sin validar monto > 0
    conn = get_db()
    conn.execute(f"UPDATE usuarios SET saldo=saldo-{monto} WHERE id={session['user_id']}")
    conn.execute(f"UPDATE usuarios SET saldo=saldo+{monto} WHERE username='{destino}'")
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "monto": float(monto), "a": destino})

@app.route('/admin/usuarios')
def listar_usuarios():
    # V9: Sin verificación de rol — cualquier usuario accede
    conn = get_db()
    data = conn.execute("SELECT id, username, password_hash, rol, saldo FROM usuarios").fetchall()
    conn.close()
    return jsonify([dict(r) for r in data])

if __name__ == '__main__':
    print("\n  Servidor VULNERABLE corriendo en http://localhost:5005\n")
    app.run(debug=True, port=5005)