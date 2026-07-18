#!/usr/bin/env python3
import bcrypt
import hashlib
import hmac
import html
import logging
import os
import sqlite3
import time
from datetime import datetime, timedelta
from urllib.parse import parse_qs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "usuarios.db")
LOG_PATH = os.path.join(BASE_DIR, "logs", "auth.log")
MAX_INTENTOS = 5
TIEMPO_BLOQUEO = 15
MAX_USER_LEN = 50
MAX_PASS_LEN = 128
# Hash bcrypt válido para igualar el trabajo cuando el usuario no existe.
HASH_DUMMY = b"$2b$12$C6UzMDM.H6dfI/f/IKcEe.5vSpL1tuP0uY5Jr7G5H4Y1x2m3n4o5a"

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def render_page(titulo, mensaje, exito=False):
    color = "#48bb78" if exito else "#e94560"
    icono = "OK" if exito else "ERROR"
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<title>{html.escape(titulo)}</title><style>
body{{font-family:Segoe UI,sans-serif;background:#1a1a2e;color:#e2e8f0;
display:grid;place-items:center;min-height:100vh;margin:0}}
.card{{background:#16213e;padding:40px;border-radius:10px;max-width:460px;
text-align:center;border:1px solid #0f3460}} h1{{color:{color}}}
p{{color:#b5bfd0}} a{{color:#e94560}}</style></head><body><div class="card">
<h1>{icono}: {html.escape(titulo)}</h1><p>{mensaje}</p>
<p><a href="/login.html">Volver al login</a></p></div></body></html>"""


def responder(titulo, mensaje, exito=False):
    print("Content-Type: text/html; charset=utf-8")
    print("Strict-Transport-Security: max-age=31536000; includeSubDomains")
    print("X-Content-Type-Options: nosniff")
    print("X-Frame-Options: DENY")
    print("Content-Security-Policy: default-src 'self'; style-src 'unsafe-inline'")
    print("Cache-Control: no-store, no-cache, must-revalidate")
    print()
    print(render_page(titulo, mensaje, exito))


metodo = os.environ.get("REQUEST_METHOD", "")
ip_cliente = os.environ.get("REMOTE_ADDR", "IP_DESCONOCIDA")
if metodo != "POST":
    logging.warning("METODO_INVALIDO method=%s ip=%s", metodo, ip_cliente)
    responder("Método no permitido", "Solo se acepta POST para el login.")
    raise SystemExit

form = parse_qs(os.environ.get("CGI_BODY", ""), keep_blank_values=True)
usuario = form.get("usuario", [""])[0].strip()
password = form.get("password", [""])[0]

if not usuario or not password:
    responder("Datos incompletos", "Completa usuario y contraseña.")
    raise SystemExit
if len(usuario) > MAX_USER_LEN or len(password) > MAX_PASS_LEN:
    logging.warning("INPUT_INVALIDO ip=%s", ip_cliente)
    responder("Datos inválidos", "Los datos superan el límite permitido.")
    raise SystemExit

try:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, usuario, hash_password, rol, activo, intentos_fallidos, "
        "bloqueado_hasta FROM usuarios WHERE usuario = ?",
        (usuario,),
    )
    fila = cursor.fetchone()
except sqlite3.Error:
    logging.exception("ERROR_BD")
    responder("Error del sistema", "Ocurrió un error interno.")
    raise SystemExit

if fila and fila["bloqueado_hasta"]:
    try:
        hasta = datetime.strptime(fila["bloqueado_hasta"], "%Y-%m-%d %H:%M:%S")
        if datetime.now() < hasta:
            logging.warning("CUENTA_BLOQUEADA usuario=%s ip=%s", usuario, ip_cliente)
            conn.close()
            responder(
                "Cuenta bloqueada temporalmente",
                "Espera antes de realizar un nuevo intento.",
            )
            raise SystemExit
        cursor.execute(
            "UPDATE usuarios SET intentos_fallidos=0, bloqueado_hasta=NULL "
            "WHERE usuario=?",
            (usuario,),
        )
        conn.commit()
    except ValueError:
        pass

hash_guardado = fila["hash_password"].encode() if fila else HASH_DUMMY
try:
    password_valido = bcrypt.checkpw(password.encode(), hash_guardado)
except ValueError:
    # Mantener una operación costosa incluso si un hash almacenado fuera inválido.
    hashlib.pbkdf2_hmac("sha256", password.encode(), b"dummy-salt", 200_000)
    password_valido = False
password_valido = bool(fila) and password_valido

if fila and password_valido and fila["activo"]:
    cursor.execute(
        "UPDATE usuarios SET intentos_fallidos=0, bloqueado_hasta=NULL "
        "WHERE usuario=?",
        (usuario,),
    )
    conn.commit()
    conn.close()
    logging.info("AUTH_SUCCESS usuario=%s rol=%s ip=%s", usuario, fila["rol"], ip_cliente)
    responder(
        "Acceso concedido",
        "Bienvenido. Rol: <strong>"
        + html.escape(fila["rol"])
        + "</strong>.",
        True,
    )
else:
    if fila:
        intentos = fila["intentos_fallidos"] + 1
        if intentos >= MAX_INTENTOS:
            hasta = (datetime.now() + timedelta(minutes=TIEMPO_BLOQUEO)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            cursor.execute(
                "UPDATE usuarios SET intentos_fallidos=?, bloqueado_hasta=? "
                "WHERE usuario=?",
                (intentos, hasta, usuario),
            )
            mensaje = (
                f"Cuenta bloqueada temporalmente durante {TIEMPO_BLOQUEO} minutos."
            )
            logging.warning(
                "CUENTA_BLOQUEADA usuario=%s intentos=%s ip=%s",
                usuario,
                intentos,
                ip_cliente,
            )
        else:
            cursor.execute(
                "UPDATE usuarios SET intentos_fallidos=? WHERE usuario=?",
                (intentos, usuario),
            )
            mensaje = (
                "Credenciales incorrectas. "
                f"Quedan {MAX_INTENTOS - intentos} intento(s)."
            )
            logging.warning(
                "AUTH_FAILURE usuario=%s intento=%s/%s ip=%s",
                usuario,
                intentos,
                MAX_INTENTOS,
                ip_cliente,
            )
        conn.commit()
    else:
        mensaje = "Credenciales incorrectas."
        logging.warning("AUTH_FAILURE usuario=no_encontrado ip=%s", ip_cliente)
    conn.close()
    time.sleep(0.1)
    responder("Acceso denegado", mensaje)
