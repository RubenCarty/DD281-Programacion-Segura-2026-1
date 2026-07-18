#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════
# login_seguro.py — VERSION FINAL COMPATIBLE PYTHON 3.14 (CGI FIXED)
# DD281 — Programación Segura
# ══════════════════════════════════════════════════════════════════

import sqlite3
import bcrypt
import html
import os
import time
import logging
import sys
sys.stdout.reconfigure(encoding='utf-8')
from urllib.parse import parse_qs
from datetime import datetime, timedelta

# ── RUTAS ──────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "db", "usuarios.db")
LOG_PATH = os.path.join(BASE_DIR, "logs", "auth.log")

# Crear carpeta logs si no existe
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

# ── LOGGING ────────────────────────────────────────────────────────
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# ── SEGURIDAD ──────────────────────────────────────────────────────
MAX_INTENTOS   = 5
TIEMPO_BLOQUEO = 15
MAX_USER_LEN   = 50
MAX_PASS_LEN   = 128

# ── HEADERS HTTP ───────────────────────────────────────────────────
print("Content-Type: text/html; charset=utf-8")
print("Strict-Transport-Security: max-age=31536000; includeSubDomains")
print("X-Content-Type-Options: nosniff")
print("X-Frame-Options: DENY")
print("X-XSS-Protection: 1; mode=block")
print("Cache-Control: no-store, no-cache, must-revalidate")
print()

# ── HTML TEMPLATE ──────────────────────────────────────────────────
def render_page(titulo: str, mensaje: str, exito: bool = False) -> str:
    color = "#48bb78" if exito else "#e94560"
    icono = "OK" if exito else "ERROR"

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>{html.escape(titulo)}</title>
<style>
body {{
    font-family: Arial;
    background: #1a1a2e;
    color: #e2e8f0;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    margin:0;
}}
.card {{
    background:#16213e;
    padding:30px;
    border-radius:10px;
    text-align:center;
    border:1px solid #0f3460;
}}
h1 {{ color:{color}; }}
a {{ color:#e94560; }}
</style>
</head>
<body>
<div class="card">
<h1>{icono} {html.escape(titulo)}</h1>
<p>{mensaje}</p>
<br>
<a href="/login.html">← Volver al login</a>
</div>
</body>
</html>"""

# ── 1. SOLO POST ───────────────────────────────────────────────────
request_method = os.environ.get("REQUEST_METHOD", "")

if request_method != "POST":
    print(render_page("Método no permitido", "Solo POST"))
    exit()

# ── 2. LECTURA CGI (FIX WINDOWS + PYTHON 3.14) ─────────────────────
try:
    content_length = int(os.environ.get("CONTENT_LENGTH", "0"))

    if content_length > 0:
        raw_data = sys.stdin.read(content_length)
    else:
        raw_data = ""

except Exception as e:
    logging.error(f"ERROR_LEYENDO_POST: {str(e)}")
    raw_data = ""

params = parse_qs(raw_data)

usuario_raw = params.get("usuario", [""])[0]
password_raw = params.get("password", [""])[0]
token_recibido = params.get("csrf_token", [""])[0]

# NUEVA LÍNEA: Captura el token del formulario
token_recibido = params.get("csrf_token", [""])[0]

usuario  = html.escape(usuario_raw.strip())
password = password_raw

# NUEVA VALIDACIÓN: Verificar el Token CSRF de forma segura
import hmac
TOKEN_ESPERADO = "4a8b92c4e1d3f5a7b93021f4e5d6c7b8a901ef23cd45bf6789abcdef01234567"

if not hmac.compare_digest(token_recibido, TOKEN_ESPERADO):
    IP_CLIENTE = os.environ.get("REMOTE_ADDR", "?")
    logging.warning(f"POSIBLE_ATAQUE_CSRF ip={IP_CLIENTE}")
    print(render_page("Error de Seguridad", "Token CSRF inválido o ausente."))
    exit()
# ───────────────────────────────────────────────────────────────────

if not usuario or not password:
    print(render_page("Error", "Datos incompletos"))
    exit()

if len(usuario) > MAX_USER_LEN or len(password) > MAX_PASS_LEN:
    print(render_page("Error", "Datos demasiado largos"))
    exit()

IP_CLIENTE = os.environ.get("REMOTE_ADDR", "?")

# ── 3. CONSULTA BASE DE DATOS ──────────────────────────────────────
try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, usuario, hash_password, rol, activo,
               intentos_fallidos, bloqueado_hasta
        FROM usuarios WHERE usuario = ?
    """, (usuario,))

    fila = cursor.fetchone()

except Exception as e:
    logging.error(f"DB_ERROR {str(e)}")
    print(render_page("Error", "Error interno del sistema"))
    exit()

# ── 4. VALIDACIÓN BCRYPT ───────────────────────────────────────────
HASH_DUMMY = b"$2b$12$invalidhashXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
hash_almacenado = fila[2].encode() if fila else HASH_DUMMY

try:
    password_ok = bcrypt.checkpw(password.encode(), hash_almacenado)
except:
    password_ok = False

if not fila:
    password_ok = False

# ── 5. LOGIN EXITOSO ───────────────────────────────────────────────
if fila and password_ok and fila[4] == 1:

    cursor.execute("""
        UPDATE usuarios
        SET intentos_fallidos=0, bloqueado_hasta=NULL
        WHERE usuario=?
    """, (usuario,))
    conn.commit()

    logging.info(f"LOGIN_OK usuario={usuario} ip={IP_CLIENTE}")

    print(render_page(
        "Acceso correcto",
        f"Bienvenido <b>{fila[3]}</b>",
        True
    ))

    conn.close()
    exit()

# ── 6. LOGIN FALLIDO ───────────────────────────────────────────────
if fila:
    intentos = fila[5] + 1

    if intentos >= MAX_INTENTOS:
        bloqueo = (datetime.now() + timedelta(minutes=TIEMPO_BLOQUEO))
        bloqueo_str = bloqueo.strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            UPDATE usuarios
            SET intentos_fallidos=?, bloqueado_hasta=?
            WHERE usuario=?
        """, (intentos, bloqueo_str, usuario))

        conn.commit()

        mensaje = "Cuenta bloqueada por intentos fallidos"

    else:
        cursor.execute("""
            UPDATE usuarios
            SET intentos_fallidos=?
            WHERE usuario=?
        """, (intentos, usuario))

        conn.commit()

        mensaje = f"Credenciales incorrectas. Intentos restantes: {MAX_INTENTOS - intentos}"

else:
    mensaje = "Credenciales incorrectas."

logging.warning(f"LOGIN_FAIL usuario={usuario} ip={IP_CLIENTE}")

conn.close()
time.sleep(0.5)

print(render_page("Acceso denegado", mensaje))