#!/usr/bin/env python3
"""
app_vulnerable.py — Aplicación con vulnerabilidades INTENCIONALES para laboratorio.
PROPÓSITO EDUCATIVO ÚNICAMENTE — NUNCA usar en producción.
"""
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = "tienda.db"

def get_db():
    """Conecta a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENDPOINT 1: Login — SQL Injection clásico
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.route('/login', methods=['POST'])
def login_inseguro():
    """
    VULNERABLE A: SQL Injection clásico

    Prueba estos payloads en el campo 'usuario':
    - admin'--          → Acceso sin contraseña
    - ' OR '1'='1'--    → Acceso con cualquier contraseña
    - ' OR 1=1--        → Alternativa sin comillas en el valor
    """
    data = request.json or {}
    usuario  = data.get('usuario', '')
    password = data.get('password', '')

    # VULNERABILIDAD: concatenación directa del input en SQL
    query = f"SELECT id, usuario, rol FROM usuarios WHERE usuario='{usuario}' AND password='{password}'"

    print(f"[DEBUG] Consulta ejecutada: {query}")

    try:
        conn = get_db()
        cursor = conn.cursor()
        resultado = cursor.execute(query).fetchone()
        conn.close()

        if resultado:
            return jsonify({
                "status": "success",
                "mensaje": f"Bienvenido {resultado['usuario']}",
                "rol": resultado['rol'],
                "query_debug": query
            })
        return jsonify({"status": "error", "mensaje": "Credenciales incorrectas"})

    except sqlite3.Error as e:
        return jsonify({"status": "error", "error_bd": str(e), "query": query}), 500

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENDPOINT 2: Buscar productos — UNION-based SQLi
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.route('/buscar', methods=['GET'])
def buscar_inseguro():
    """
    VULNERABLE A: UNION-based SQL Injection

    Payload para extraer usuarios:
    ?categoria=electronica' UNION SELECT id,usuario,password,rol,email FROM usuarios--
    """
    categoria = request.args.get('categoria', '')

    conn = get_db()
    cursor = conn.cursor()

    query = f"SELECT id, nombre, precio, categoria, stock FROM productos WHERE categoria='{categoria}'"
    print(f"[DEBUG] Consulta: {query}")

    try:
        resultados = cursor.execute(query).fetchall()
        conn.close()
        return jsonify({
            "productos": [dict(r) for r in resultados],
            "query_debug": query,
            "total": len(resultados)
        })
    except sqlite3.Error as e:
        return jsonify({"error": str(e), "query": query}), 500

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENDPOINT 3: Diagnóstico — Command Injection
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.route('/diagnostico', methods=['GET'])
def diagnostico_inseguro():
    """
    VULNERABLE A: Command Injection

    Payload de ataque:
    ?host=127.0.0.1; ls -la
    ?host=127.0.0.1 && whoami
    """
    host = request.args.get('host', '127.0.0.1')

    import subprocess
    resultado = subprocess.run(
        f"ping -c 2 {host}",
        shell=True,
        capture_output=True,
        text=True,
        timeout=10
    )

    return jsonify({
        "host": host,
        "output": resultado.stdout,
        "errores": resultado.stderr
    })

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENDPOINT 4 (Parte 3): Perfil — Blind SQL Injection (boolean-based)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.route('/perfil/<int:user_id>')
def perfil(user_id):
    """
    Este endpoint muestra información del usuario pero NO errores de BD.
    ¿Puedes inferir la contraseña del admin usando Blind SQLi?

    NOTA DE DISEÑO: la versión original del enunciado inyectaba en un
    ORDER BY, pero SQLite (y la mayoría de motores) omiten evaluar la
    expresión de ORDER BY cuando el resultado ya tiene una sola fila
    (no hay nada que ordenar), así que ese payload nunca cambia la
    respuesta y la técnica no es explotable. Aquí se usa la variante
    clásica y sí funcional: inyectar una condición booleana adicional
    en el WHERE, que si es falsa hace que la fila deje de "existir".
    """
    conn = get_db()
    # Nota: user_id es int, así que está protegido de SQLi básico
    # Pero el parámetro GET 'filtro' no lo está
    filtro = request.args.get('filtro', '1=1')

    # VULNERABILIDAD: condición booleana concatenada directamente en el WHERE
    query = f"SELECT usuario, email, rol FROM usuarios WHERE id={user_id} AND ({filtro})"
    try:
        resultado = conn.execute(query).fetchone()
        conn.close()
        if resultado:
            return jsonify({"existe": True, "usuario": resultado[0]})
        return jsonify({"existe": False})
    except Exception:
        # Silencia los errores — hace el ataque más difícil (Blind)
        conn.close()
        return jsonify({"existe": False})

if __name__ == '__main__':
    print("APLICACION VULNERABLE — Solo para uso educativo en laboratorio")
    print("   Acceder en: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
