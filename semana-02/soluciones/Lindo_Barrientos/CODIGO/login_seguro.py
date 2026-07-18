#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════
# login_seguro.py — IMPLEMENTACIÓN SEGURA DEL LOGIN CON CGI
# Semana 2 — Programación Segura DD281
# ══════════════════════════════════════════════════════════════════
import cgi
import cgitb
import sqlite3
import bcrypt
import html
import os
import time
import logging
from datetime import datetime, timedelta

# Configuración de rutas (relativas al directorio del proyecto)
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH    = os.path.join(BASE_DIR, "db", "usuarios.db")
LOG_PATH   = os.path.join(BASE_DIR, "logs", "auth.log")

# Configuración de logging de seguridad
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Constantes de seguridad
MAX_INTENTOS    = 5
TIEMPO_BLOQUEO  = 15   # minutos
MAX_USER_LEN    = 50
MAX_PASS_LEN    = 128

# ── HEADERS HTTP DE SEGURIDAD ──────────────────────────────────────
# Estos headers se envían antes que cualquier contenido HTML.
# Deben estar ANTES de la línea en blanco del Content-Type.
print("Content-Type: text/html; charset=utf-8")
print("Strict-Transport-Security: max-age=31536000; includeSubDomains")
print("X-Content-Type-Options: nosniff")
print("X-Frame-Options: DENY")
print("X-XSS-Protection: 1; mode=block")
print("Cache-Control: no-store, no-cache, must-revalidate")
print()   # Línea en blanco OBLIGATORIA — separa headers de body

# ── PLANTILLA HTML ─────────────────────────────────────────────────
def render_page(titulo: str, mensaje: str, exito: bool = False) -> str:
    color = "#48bb78" if exito else "#e94560"
    icono = "✅" if exito else "❌"
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{html.escape(titulo)}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #1a1a2e; 
               color: #e2e8f0; display: flex; justify-content: center; 
               align-items: center; min-height: 100vh; margin: 0; }}
        .card {{ background: #16213e; padding: 40px; border-radius: 10px; 
                max-width: 420px; text-align: center; 
                border: 1px solid #0f3460; }}
        h1 {{ color: {color}; }}
        p {{ color: #a0aec0; margin-top: 10px; }}
        a {{ color: #e94560; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>{icono} {html.escape(titulo)}</h1>
        <p>{mensaje}</p>
        <p style="margin-top:20px;"><a href="/login.html">← Volver al login</a></p>
    </div>
</body>
</html>"""

# ── 1. VERIFICAR MÉTODO HTTP ───────────────────────────────────────
request_method = os.environ.get('REQUEST_METHOD', '')
if request_method != 'POST':
    logging.warning(f"MÉTODO_INVÁLIDO method={request_method} "
                    f"ip={os.environ.get('REMOTE_ADDR','?')}")
    print(render_page("Método no permitido", 
                      "Solo se acepta POST para el login."))
    exit(0)

# ── 2. VERIFICAR HTTPS ─────────────────────────────────────────────
# En producción real, verificar HTTPS es crítico.
# En laboratorio local con Python HTTP, HTTPS lo maneja el servidor.
# Puedes comentar este bloque si tu servidor no expone la variable HTTPS.
# https_env = os.environ.get('HTTPS', '')
# if https_env != 'on':
#     logging.warning(f"ACCESO_HTTP ip={os.environ.get('REMOTE_ADDR','?')}")
#     print(render_page("HTTPS requerido", 
#                       "Este sistema requiere conexión cifrada (HTTPS)."))
#     exit(0)

# ── 3. OBTENER Y VALIDAR INPUTS ────────────────────────────────────
form = cgi.FieldStorage()
usuario_raw  = form.getvalue("usuario", "")
password_raw = form.getvalue("password", "")

# Sanitización: escapar HTML para uso en respuestas, strip de espacios
usuario  = html.escape(str(usuario_raw).strip())
password = str(password_raw)   # Las contraseñas NO se escapan — se tratan como bytes

# Validación de longitud (previene ataques de desbordamiento / DoS)
if not usuario or not password:
    print(render_page("Datos incompletos", 
                      "Por favor, completa usuario y contraseña."))
    exit(0)

if len(usuario) > MAX_USER_LEN or len(password) > MAX_PASS_LEN:
    logging.warning(f"INPUT_INVÁLIDO usuario={usuario[:20]} "
                    f"ip={os.environ.get('REMOTE_ADDR','?')}")
    print(render_page("Datos inválidos", 
                      "Los datos ingresados superan el límite permitido."))
    exit(0)

# IP del cliente para logging
IP_CLIENTE = os.environ.get('REMOTE_ADDR', 'IP_DESCONOCIDA')

# ── 4. CONSULTAR BD CON PREPARED STATEMENT ────────────────────────
try:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # Acceso por nombre de columna
    cursor = conn.cursor()

    # NUNCA concatenar usuario directamente — usar parámetros (?)
    cursor.execute(
        "SELECT id, usuario, hash_password, rol, activo, "
        "intentos_fallidos, bloqueado_hasta "
        "FROM usuarios WHERE usuario = ?",
        (usuario,)
    )
    fila = cursor.fetchone()

except sqlite3.Error as e:
    logging.error(f"ERROR_BD: {str(e)}")
    print(render_page("Error del sistema", 
                      "Ocurrió un error interno. Intenta más tarde."))
    exit(0)

# ── 5. VERIFICAR BLOQUEO DE CUENTA ────────────────────────────────
if fila and fila['bloqueado_hasta']:
    try:
        bloqueado_hasta = datetime.strptime(
            fila['bloqueado_hasta'], '%Y-%m-%d %H:%M:%S'
        )
        if datetime.now() < bloqueado_hasta:
            tiempo_restante = int(
                (bloqueado_hasta - datetime.now()).total_seconds() / 60
            )
            logging.warning(f"CUENTA_BLOQUEADA usuario={usuario} ip={IP_CLIENTE}")
            print(render_page(
                "Cuenta bloqueada temporalmente",
                f"Tu cuenta está bloqueada por intentos fallidos. "
                f"Intenta en {tiempo_restante} minuto(s)."
            ))
            conn.close()
            exit(0)
        else:
            # El bloqueo expiró — resetear contador
            cursor.execute(
                "UPDATE usuarios SET intentos_fallidos=0, bloqueado_hasta=NULL "
                "WHERE usuario=?", (usuario,)
            )
            conn.commit()
    except ValueError:
        pass   # Formato de fecha inválido en BD — continuar

# ── 6. VERIFICAR CONTRASEÑA CON BCRYPT ────────────────────────────
# IMPORTANTE: Para prevenir timing attacks, siempre ejecutamos checkpw
# aunque el usuario no exista, usando un hash dummy.
# Si solo ejecutamos el if cuando el usuario existe, un atacante puede
# medir el tiempo de respuesta para saber si el usuario es válido.

HASH_DUMMY = b'$2b$12$invalidhashXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

hash_almacenado = fila['hash_password'].encode('utf-8') if fila else HASH_DUMMY

try:
    password_valido = bcrypt.checkpw(
        password.encode('utf-8'), 
        hash_almacenado
    )
except Exception:
    password_valido = False

# Si el usuario no existe, marcamos como inválido independientemente
if not fila:
    password_valido = False

# ── 7. MANEJAR RESULTADO ──────────────────────────────────────────
if fila and password_valido and fila['activo']:

    # Login exitoso — resetear contador de intentos fallidos
    cursor.execute(
        "UPDATE usuarios SET intentos_fallidos=0, bloqueado_hasta=NULL "
        "WHERE usuario=?",
        (usuario,)
    )
    conn.commit()
    conn.close()

    logging.info(f"AUTH_SUCCESS usuario={usuario} rol={fila['rol']} ip={IP_CLIENTE}")

    print(render_page(
        "Acceso concedido",
        f"Bienvenido. Has iniciado sesión como <strong>{html.escape(fila['rol'])}</strong>. "
        f"<br><br>En un sistema completo, aquí se generaría un token de sesión "
        f"y se redireccionaría al dashboard.",
        exito=True
    ))

else:

    # Login fallido
    if fila:
        nuevos_intentos = fila['intentos_fallidos'] + 1

        if nuevos_intentos >= MAX_INTENTOS:
            # Bloquear la cuenta
            bloqueado_hasta = (
                datetime.now() + timedelta(minutes=TIEMPO_BLOQUEO)
            ).strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute(
                "UPDATE usuarios SET intentos_fallidos=?, bloqueado_hasta=? "
                "WHERE usuario=?",
                (nuevos_intentos, bloqueado_hasta, usuario)
            )
            conn.commit()
            logging.warning(
                f"CUENTA_BLOQUEADA usuario={usuario} "
                f"intentos={nuevos_intentos} ip={IP_CLIENTE} "
                f"hasta={bloqueado_hasta}"
            )
            mensaje_error = (
                f"Tu cuenta ha sido bloqueada por {MAX_INTENTOS} intentos fallidos. "
                f"Intenta en {TIEMPO_BLOQUEO} minutos."
            )
        else:
            cursor.execute(
                "UPDATE usuarios SET intentos_fallidos=? WHERE usuario=?",
                (nuevos_intentos, usuario)
            )
            conn.commit()
            logging.warning(
                f"AUTH_FAILURE usuario={usuario} "
                f"intento={nuevos_intentos}/{MAX_INTENTOS} ip={IP_CLIENTE}"
            )
            # Mensaje GENÉRICO — no revela si el usuario existe
            mensaje_error = (
                "Credenciales incorrectas. "
                f"Te quedan {MAX_INTENTOS - nuevos_intentos} intento(s) "
                f"antes del bloqueo temporal."
            )
    else:
        logging.warning(
            f"AUTH_FAILURE usuario={usuario} (no existe) ip={IP_CLIENTE}"
        )
        # Mismo mensaje que si el usuario existe — evita user enumeration
        mensaje_error = "Credenciales incorrectas."

    conn.close()

    # Pequeña penalización de tiempo (dificulta ataques de fuerza bruta automatizados)
    time.sleep(0.5)

    print(render_page("Acceso denegado", mensaje_error))
