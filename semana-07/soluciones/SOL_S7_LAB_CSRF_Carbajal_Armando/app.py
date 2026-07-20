from flask import Flask, request, session, jsonify, redirect
import sqlite3
import hashlib
import os
import logging

app = Flask(__name__)
app.secret_key = "banco2024"

# Sin SESSION_COOKIE_SAMESITE
# Sin SESSION_COOKIE_HTTPONLY

# Credenciales de producción hardcodeadas
DB_PASS = "BancoAdmin2024"
DB_URL = f"postgresql://admin:{DB_PASS}@prod-db.banco.pe:5432/clientes"

logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def inicio():
    return "Banco Nacional funcionando"


@app.route('/login', methods=['POST'])
def login():

    username = request.form.get('username')
    password = request.form.get('password')

    # Hash MD5 de la contraseña
    password_hash = hashlib.md5(password.encode()).hexdigest()

    conn = sqlite3.connect('banco.db')

    # Consulta concatenada (SQL Injection)
    user = conn.execute(
        f"SELECT * FROM usuarios WHERE username='{username}' AND password_hash='{password_hash}'"
    ).fetchone()

    conn.close()

    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['rol'] = 'cliente'      # Vulnerabilidad

        logging.debug(
            f"Login exitoso: user={username}, password={password}"
        )

        return jsonify({"mensaje":"Login exitoso"})

    return jsonify({"error":"Credenciales incorrectas"}),401


@app.route('/transferir', methods=['POST'])
def transferir():

    if not session.get('user_id'):
        return redirect('/login')

    destino=request.form.get('destino')
    monto=request.form.get('monto')

    conn=sqlite3.connect('banco.db')

    conn.execute(
        f"UPDATE cuentas SET saldo=saldo-{monto} WHERE usuario_id={session['user_id']}"
    )

    conn.execute(
        f"UPDATE cuentas SET saldo=saldo+{monto} WHERE numero='{destino}'"
    )

    conn.commit()
    conn.close()

    return jsonify({"ok":True})


@app.route('/admin/usuarios')
def listar_usuarios():

    conn=sqlite3.connect('banco.db')

    usuarios=conn.execute(
        "SELECT id,username,password_hash,saldo,email FROM usuarios"
    ).fetchall()

    conn.close()

    return jsonify(usuarios)


if __name__=="__main__":
    app.run(debug=True)