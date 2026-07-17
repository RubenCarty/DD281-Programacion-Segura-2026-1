#!/usr/bin/env python3
"""
app_segura.py — Implementación SEGURA de los mismos endpoints.
Todos los TODO han sido completados.
"""

import sqlite3
import subprocess
import ipaddress
import re
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = "tienda.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENDPOINT 1 SEGURO: Login con prepared statement
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.route("/login", methods=["POST"])
def login_seguro():
    data = request.json or {}
    usuario = data.get("usuario", "").strip()
    password = data.get("password", "")

    # TODO 1: Validar longitud del input (usuario max 50 chars, password max 128)
    if (
        len(usuario) == 0
        or len(usuario) > 50
        or len(password) == 0
        or len(password) > 128
    ):
        return jsonify({"status": "error", "mensaje": "Credenciales inválidas"}), 400

    # TODO 2: Validar formato del usuario (solo alfanumérico + guion bajo)
    if not re.match(r"^[a-zA-Z0-9_]{3,50}$", usuario):
        return jsonify({"status": "error", "mensaje": "Credenciales inválidas"}), 400

    conn = get_db()
    cursor = conn.cursor()

    # TODO 3: Prepared statement — el driver separa código SQL de los datos,
    # así que un valor como "admin'--" se trata como texto literal, nunca como
    # sintaxis SQL.
    query = "SELECT id, usuario, rol FROM usuarios WHERE usuario=? AND password=?"
    resultado = cursor.execute(query, (usuario, password)).fetchone()
    conn.close()

    if resultado:
        return jsonify(
            {"status": "success", "mensaje": f"Bienvenido {resultado['usuario']}"}
        )
    # Mensaje genérico: no revela si el problema fue el usuario o la contraseña
    return jsonify({"status": "error", "mensaje": "Credenciales inválidas"}), 401


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENDPOINT 2 SEGURO: Buscar con prepared statement
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.route("/buscar", methods=["GET"])
def buscar_seguro():
    categoria = request.args.get("categoria", "").strip()

    # TODO 4: Validar que categoria solo contenga letras (a-z) y guion bajo
    if categoria and not re.match(r"^[a-z_]{1,30}$", categoria):
        return jsonify({"error": "Categoría inválida"}), 400

    conn = get_db()
    cursor = conn.cursor()

    # TODO 5: Prepared statement para la búsqueda
    query = (
        "SELECT id, nombre, precio, categoria, stock FROM productos WHERE categoria=?"
    )
    resultados = cursor.execute(query, (categoria,)).fetchall()
    conn.close()

    return jsonify(
        {"productos": [dict(r) for r in resultados], "total": len(resultados)}
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENDPOINT 3 SEGURO: Diagnóstico sin Command Injection
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.route("/diagnostico", methods=["GET"])
def diagnostico_seguro():
    host_raw = request.args.get("host", "").strip()

    # TODO 6: Validar que es una IP pública válida.
    # Se usa ipaddress.ip_address para rechazar cualquier cosa que no sea una
    # IP bien formada (esto ya bloquea "; ls -la" por sí solo), y además se
    # rechazan rangos privados/loopback/reservados para evitar SSRF interno.
    try:
        ip = ipaddress.ip_address(host_raw)
    except ValueError:
        return jsonify({"error": "Host inválido: debe ser una dirección IP"}), 400

    if (
        ip.is_private
        or ip.is_loopback
        or ip.is_reserved
        or ip.is_link_local
        or ip.is_multicast
    ):
        return jsonify(
            {"error": "No se permiten IPs privadas, de loopback o reservadas"}
        ), 400

    # TODO 7: Ejecutar ping con subprocess en modo lista (SIN shell=True).
    # Al pasar los argumentos como lista y no usar shell=True, el sistema
    # operativo no interpreta ";", "&&", "|", etc. como separadores de
    # comandos: se pasan literalmente como argumentos de "ping".
    try:
        resultado = subprocess.run(
            ["ping", "-c", "2", str(ip)],
            shell=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Tiempo de espera agotado"}), 504

    return jsonify(
        {"host": str(ip), "output": resultado.stdout, "errores": resultado.stderr}
    )


if __name__ == "__main__":
    print("Aplicación SEGURA — http://127.0.0.1:5001")
    app.run(debug=False, port=5001)
