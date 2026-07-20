# GUÍA DE LABORATORIO — SEMANA 2
# IMPLEMENTACIÓN DE LOGIN SEGURO CON CGI Y SSL
## Programación Segura (DD281)

---

**Nombre del estudiante:** giancarlos alegria ibarra

**Grupo / Sección:** 8 ciclo

**Fecha de entrega:** 14/06/2026

---

## INFORMACIÓN DEL LABORATORIO

| Campo | Detalle |
|---|---|
| **Duración estimada** | 90-120 minutos |
| **Modalidad** | Individual o parejas |
| **Entregable** | Carpeta comprimida con código + capturas + informe |
| **Herramientas requeridas** | Python 3.8+, OpenSSL, navegador web, terminal |
| **Sistema operativo** | Linux (Ubuntu/Debian) recomendado. Windows con WSL2. macOS aceptado. |

---

## OBJETIVOS DEL LABORATORIO

Al finalizar este laboratorio, el estudiante será capaz de:

1. Configurar un servidor web con Python que soporte CGI.
2. Generar un certificado SSL autofirmado con OpenSSL.
3. Implementar un script CGI de login que use bcrypt para verificar contraseñas.
4. Identificar diferencias de seguridad entre una implementación insegura y una segura.
5. Verificar el funcionamiento del certificado SSL en el navegador.

---

## PRERREQUISITOS

### Software necesario

Verifica que tienes instalado lo siguiente antes de comenzar:

```bash
# Verificar Python 3
python3 --version    # Debe ser 3.8 o superior

# Verificar OpenSSL
openssl version      # Debe ser 1.1.1 o superior

# Verificar pip
pip3 --version

# Instalar dependencias Python
pip3 install bcrypt

# En Ubuntu/Debian — instalar OpenSSL si no está:
# sudo apt-get update && sudo apt-get install openssl

# En macOS con Homebrew:
# brew install openssl
```

---
## Captura 1
![PreRequisitos](Capturas/SS01_Prerequisitos.png)

## ESTRUCTURA DEL PROYECTO

Al finalizar el laboratorio, tu proyecto debe tener esta estructura:

```
lab_login_seguro/
├── certs/
│   ├── server.key          ← Clave privada SSL (¡no subir a GitHub!)
│   ├── server.csr          ← Certificate Signing Request
│   └── server.crt          ← Certificado SSL autofirmado
├── cgi-bin/
│   ├── login_inseguro.py   ← Script CGI inseguro (para análisis)
│   └── login_seguro.py     ← Script CGI seguro (tu implementación)
├── www/
│   ├── login.html          ← Formulario HTML del login
│   └── estilos.css         ← Estilos básicos
├── db/
│   └── usuarios.db         ← Base de datos SQLite
├── logs/
│   └── auth.log            ← Log de autenticación
├── setup_db.py             ← Script para inicializar la BD
└── servidor.py             ← Servidor HTTPS con CGI
```


---

## PARTE 1 — CONFIGURACIÓN DEL ENTORNO

### Paso 1.1 — Crear la estructura del proyecto

Abre una terminal y ejecuta:

```bash
# Crear directorio del proyecto
mkdir -p lab_login_seguro/{certs,cgi-bin,www,db,logs}
cd lab_login_seguro

# Dar permisos correctos al directorio de logs
chmod 755 logs/

echo "Estructura creada correctamente"
ls -la
```

**Captura de pantalla requerida:** Captura el resultado de `ls -la` mostrando las carpetas creadas.

## Captura 2
![PreRequisitos](Capturas/SS02_Estructura.png)

---

### Paso 1.2 — Generar el Certificado SSL Autofirmado

```bash
# Desde el directorio lab_login_seguro/
cd certs/

# PASO A: Generar clave privada RSA de 2048 bits
openssl genrsa -out server.key 2048

echo "✓ Clave privada generada: server.key"
ls -la server.key   # Verifica el tamaño (~1.7KB)

# PASO B: Generar Certificate Signing Request (CSR)
# El comando pedirá información. Completa así:
# Country Name: PE
# State: Lima
# Locality: Lima
# Organization Name: Universidad Autonoma
# Organizational Unit Name: Ingenieria
# Common Name: localhost   ← MUY IMPORTANTE: debe ser "localhost" para labs locales
# Email: (puedes dejarlo vacío)
openssl req -new -key server.key -out server.csr

# Alternativa: pasar todo en una línea (no interactivo)
# openssl req -new -key server.key -out server.csr \
#   -subj "/C=PE/ST=Lima/L=Lima/O=UnivAutonoma/CN=localhost"

# PASO C: Autofirmar el certificado (válido 365 días)
openssl x509 -req -days 365 -in server.csr \
  -signkey server.key -out server.crt

echo "✓ Certificado generado: server.crt"

# PASO D: Verificar el certificado generado
echo ""
echo "=== INFORMACIÓN DEL CERTIFICADO ==="
openssl x509 -in server.crt -text -noout | grep -E "Subject:|Validity:|Not Before:|Not After:"

# PASO E: Proteger la clave privada
chmod 600 server.key
echo "✓ Permisos de clave privada: $(ls -la server.key | awk '{print $1}')"

cd ..
```

**Preguntas de reflexión 1.2:**

a) ¿Qué diferencia de seguridad hay entre los permisos `chmod 600` y `chmod 644` para `server.key`?

   *Tu respuesta:* chmod 600 permite que solo el propietario pueda leer y modificar la clave privada, mientras que chmod 644 permite que otros usuarios la puedan leer. Para server.key es más seguro usar 600

b) ¿Por qué el campo `Common Name` del certificado debe ser `localhost` en este laboratorio? ¿Qué pasaría si pones otro valor?

   *Tu respuesta:* Porque el servidor del laboratorio se ejecuta en https://localhost:8443. Si se coloca otro nombre, el certificado no coincidirá con la dirección usada y el navegador mostrará una advertencia de seguridad.

c) El archivo `server.csr` ya no es necesario después de generar el certificado. ¿Qué harías con él en un entorno de producción?

   *Tu respuesta:* Lo guardaría como respaldo en un lugar seguro o lo eliminaría si ya no es necesario, para evitar mantener archivos innecesarios.

---

### Paso 1.3 — Inicializar la Base de Datos

Crea el archivo `setup_db.py` en la raíz del proyecto:

```python
#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════
# setup_db.py — Inicializa la base de datos SQLite con usuarios de prueba
# ══════════════════════════════════════════════════════════════════
import sqlite3
import bcrypt
import os

DB_PATH = "db/usuarios.db"

def crear_hash(password: str) -> str:
    """Crea hash bcrypt con factor de coste 12."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def inicializar_bd():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Crear tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            hash_password TEXT NOT NULL,
            rol TEXT DEFAULT 'estudiante',
            activo INTEGER DEFAULT 1,
            intentos_fallidos INTEGER DEFAULT 0,
            bloqueado_hasta TEXT DEFAULT NULL,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Usuarios de prueba
    usuarios_test = [
        ("juan.garcia",   "MiPassword123!",  "estudiante"),
        ("maria.lopez",   "SecurePass456#",  "estudiante"),
        ("prof.rodriguez","DocPass789$",     "docente"),
        ("admin",         "AdminSuper012!",  "administrador"),
    ]
    
    print("Creando usuarios de prueba con bcrypt (factor 12)...")
    print("Esto puede tomar unos segundos por el factor de coste...\n")
    
    for usuario, password, rol in usuarios_test:
        hash_pw = crear_hash(password)
        try:
            cursor.execute(
                "INSERT INTO usuarios (usuario, hash_password, rol) VALUES (?, ?, ?)",
                (usuario, hash_pw, rol)
            )
            print(f"  ✓ Usuario '{usuario}' creado")
            print(f"    Hash: {hash_pw[:30]}...")
        except sqlite3.IntegrityError:
            print(f"  ⚠ Usuario '{usuario}' ya existe — omitido")
    
    conn.commit()
    conn.close()
    
    print(f"\n✓ Base de datos inicializada en: {DB_PATH}")
    print(f"  Tamaño: {os.path.getsize(DB_PATH)} bytes")

if __name__ == "__main__":
    inicializar_bd()
```

Ejecuta el script:

```bash
python3 setup_db.py
```

**Observa el output. ¿Cuánto tiempo tardó en crear los 4 usuarios?**

*Tu respuesta:* 2 a 5 segundos aproximadamente.

**Pregunta:** ¿Por qué tarda ese tiempo? ¿Es un defecto o una característica de seguridad?

*Tu respuesta:* Tarda ese tiempo porque estoy usando bcrypt con un nivel de coste 12, lo que hace que cada contraseña pase por varios cálculos antes de generar el hash. Eso hace que el proceso sea más lento a propósito.

No es un error ni un defecto, es una medida de seguridad. Sirve para que no sea fácil o rápido intentar adivinar contraseñas por fuerza bruta, ya que cada intento requiere más tiempo de procesamiento.

---

## PARTE 2 — EL FORMULARIO HTML

### Paso 2.1 — Crear la página de login

Crea el archivo `www/login.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Seguro — Programación Segura</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: #1a1a2e;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .login-container {
            background: #16213e;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            width: 380px;
            border: 1px solid #0f3460;
        }
        h1 {
            color: #e94560;
            text-align: center;
            margin-bottom: 8px;
            font-size: 1.5rem;
        }
        .subtitle {
            color: #7a8499;
            text-align: center;
            font-size: 0.85rem;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #a0aec0;
            margin-bottom: 6px;
            font-size: 0.9rem;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 12px 16px;
            background: #0f3460;
            border: 1px solid #1a4a7a;
            border-radius: 6px;
            color: #e2e8f0;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #e94560;
        }
        button[type="submit"] {
            width: 100%;
            padding: 14px;
            background: #e94560;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
            margin-top: 10px;
        }
        button:hover { background: #c73652; }
        .security-badge {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            margin-top: 20px;
            color: #48bb78;
            font-size: 0.8rem;
        }
        .lock-icon { font-size: 1rem; }
        .warning {
            background: #744210;
            border: 1px solid #b7791f;
            color: #fefcbf;
            padding: 10px;
            border-radius: 6px;
            font-size: 0.85rem;
            margin-bottom: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>🔐 Portal Seguro</h1>
        <p class="subtitle">Programación Segura — DD281</p>
        
        <div class="warning">
            ⚠️ Certificado autofirmado — Solo para laboratorio
        </div>
        
        <!--
            PUNTOS DE SEGURIDAD IMPLEMENTADOS EN ESTE FORMULARIO:
            1. method="post" — credenciales en body, NO en URL
            2. action apunta al script CGI seguro
            3. autocomplete="off" — evita que el navegador guarde la contraseña en caché local
            4. El formulario solo funciona con HTTPS (verificado en el backend)
        -->
        <form method="post" action="/cgi-bin/login_seguro.py" autocomplete="off">
            <div class="form-group">
                <label for="usuario">Usuario:</label>
                <input 
                    type="text" 
                    id="usuario" 
                    name="usuario" 
                    required 
                    maxlength="50"
                    placeholder="tu.usuario"
                    autocomplete="username"
                >
            </div>
            <div class="form-group">
                <label for="password">Contraseña:</label>
                <input 
                    type="password" 
                    id="password" 
                    name="password" 
                    required 
                    maxlength="128"
                    placeholder="••••••••"
                    autocomplete="current-password"
                >
            </div>
            <button type="submit">Iniciar Sesión</button>
        </form>
        
        <div class="security-badge">
            <span class="lock-icon">🔒</span>
            <span>Conexión cifrada con TLS</span>
        </div>
    </div>
</body>
</html>
```

---

## PARTE 3 — LOS SCRIPTS CGI

### Paso 3.1 — Script CGI INSEGURO (para análisis)

Crea `cgi-bin/login_inseguro.py`. Este script existe SOLO para que identifiques sus vulnerabilidades:

```python
#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════
# login_inseguro.py — SCRIPT CON VULNERABILIDADES INTENCIONALES
# PROPÓSITO: Análisis de vulnerabilidades — NO usar en producción
# ══════════════════════════════════════════════════════════════════
import cgi
import sqlite3
import os

print("Content-Type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()
usuario  = form.getvalue("usuario", "")
password = form.getvalue("password", "")

# ❌ VULNERABILIDAD 1: SQL Injection — concatenación directa
conn = sqlite3.connect("db/usuarios.db")
cursor = conn.cursor()
sql = f"SELECT * FROM usuarios WHERE usuario='{usuario}' AND hash_password='{password}'"
cursor.execute(sql)
fila = cursor.fetchone()
conn.close()

# ❌ VULNERABILIDAD 2: Comparación de contraseña sin hash
# (asume que hash_password guarda texto plano — conceptualmente inseguro)

if fila:
    # ❌ VULNERABILIDAD 3: XSS — usuario reflejado sin escapar
    # ❌ VULNERABILIDAD 4: Información excesiva en respuesta
    print(f"""
    <h1>Bienvenido {usuario}</h1>
    <p>Registro completo: {fila}</p>
    <p>Tu contraseña es: {password}</p>
    """)
else:
    # ❌ VULNERABILIDAD 5: Mensaje de error que confirma si el usuario existe
    cursor2 = sqlite3.connect("db/usuarios.db").cursor()
    existe = cursor2.execute(
        f"SELECT id FROM usuarios WHERE usuario='{usuario}'"
    ).fetchone()
    if existe:
        print("<h1>Contraseña incorrecta para ese usuario</h1>")
    else:
        print(f"<h1>El usuario '{usuario}' no existe en el sistema</h1>")
    # ❌ VULNERABILIDAD 6: Sin rate limiting ni logging de intento fallido
```

Marca los permisos correctos:

```bash
chmod 755 cgi-bin/login_inseguro.py
```

---

### Paso 3.2 — Script CGI SEGURO (tu implementación principal)

Crea `cgi-bin/login_seguro.py`:

```python
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
```

Asigna permisos:

```bash
chmod 755 cgi-bin/login_seguro.py
```

---

## PARTE 4 — EL SERVIDOR HTTPS

### Paso 4.1 — Crear el servidor con soporte SSL y CGI

Crea el archivo `servidor.py` en la raíz del proyecto:

```python
#!/usr/bin/env python3
# ══════════════════════════════════════════════════════════════════
# servidor.py — Servidor HTTPS con soporte CGI para el laboratorio
# ══════════════════════════════════════════════════════════════════
import ssl
import http.server
import os
import sys

# Directorios del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WWW_DIR  = os.path.join(BASE_DIR, "www")

# Cambiar al directorio www para servir archivos estáticos
os.chdir(BASE_DIR)

# Configuración del servidor
PUERTO    = 8443
CERT_FILE = os.path.join(BASE_DIR, "certs", "server.crt")
KEY_FILE  = os.path.join(BASE_DIR, "certs", "server.key")
CGI_DIR   = os.path.join(BASE_DIR, "cgi-bin")

class MiHandler(http.server.CGIHTTPRequestHandler):
    """Handler personalizado para servir CGI y archivos estáticos."""
    
    # Directorio de scripts CGI
    cgi_directories = ["/cgi-bin"]
    
    def translate_path(self, path):
        """Redirige / a /login.html y sirve estáticos desde www/."""
        if path == "/":
            path = "/login.html"
        
        # Si es CGI, usar la ruta base
        if path.startswith("/cgi-bin/"):
            return os.path.join(BASE_DIR, path[1:])
        
        # Archivos estáticos desde www/
        return os.path.join(WWW_DIR, path.lstrip("/"))
    
    def log_message(self, format, *args):
        """Personaliza el log del servidor."""
        print(f"[SERVIDOR] {self.address_string()} - {format % args}")

def iniciar_servidor():
    # Verificar que existen los certificados
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        print("ERROR: No se encontraron los certificados SSL.")
        print(f"  Buscando: {CERT_FILE}")
        print(f"  Buscando: {KEY_FILE}")
        print("\nEjecuta primero los comandos OpenSSL de la Parte 1.2")
        sys.exit(1)
    
    # Crear contexto SSL
    contexto_ssl = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    # Cargar certificado y clave privada
    contexto_ssl.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    
    # Opciones de seguridad del contexto SSL
    contexto_ssl.minimum_version = ssl.TLSVersion.TLSv1_2   # TLS 1.2 mínimo
    contexto_ssl.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:!aNULL')
    
    # Crear servidor HTTP
    servidor = http.server.HTTPServer(('localhost', PUERTO), MiHandler)
    
    # Envolver con SSL
    servidor.socket = contexto_ssl.wrap_socket(
        servidor.socket, 
        server_side=True
    )
    
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║           SERVIDOR HTTPS INICIADO — LABORATORIO S2              ║
╠══════════════════════════════════════════════════════════════════╣
║  URL:          https://localhost:{PUERTO}                          ║
║  CGI:          https://localhost:{PUERTO}/cgi-bin/               ║
║  Certificado:  {CERT_FILE[-40:]:40}  ║
║  TLS mínimo:   TLS 1.2                                          ║
╠══════════════════════════════════════════════════════════════════╣
║  ⚠️  El navegador mostrará alerta de certificado autofirmado.   ║
║     Acepta la excepción de seguridad para continuar.            ║
╠══════════════════════════════════════════════════════════════════╣
║  Ctrl+C para detener el servidor                                ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServidor detenido.")
        servidor.server_close()

if __name__ == "__main__":
    iniciar_servidor()
```

---

## PARTE 5 — EJECUCIÓN Y PRUEBAS

### Paso 5.1 — Iniciar el servidor

```bash
# Desde el directorio raíz del proyecto
python3 servidor.py
```

Deberías ver el banner del servidor. Si hay errores, verifica:
- Que los certificados existen en `certs/`
- Que el puerto 8443 no está en uso: `netstat -tulpn | grep 8443`

---

### Paso 5.2 — Acceder al login en el navegador

1. Abre tu navegador web
2. Navega a: `https://localhost:8443`
3. El navegador mostrará una advertencia de seguridad (certificado autofirmado)
4. En Chrome: `Avanzado` → `Continuar en localhost (no seguro)`
5. En Firefox: `Avanzado` → `Aceptar el riesgo y continuar`

## Captura 3
![PreRequisitos](Capturas/AdvertenciaChrome.png)

**¿Por qué aparece esta advertencia?**
Aparece porque el certificado SSL que estoy usando es autofirmado, es decir, no fue emitido por una autoridad de certificación confiable. El navegador no puede verificar la identidad del servidor, por eso muestra la alerta de seguridad.

Esto es normal en entornos de pruebas o laboratorio, pero no en sistemas reales en producción, donde se usan certificados válidos emitidos por entidades reconocidas.

---

### Paso 5.3 — Pruebas del sistema

Realiza cada prueba y documenta el resultado:

#### Prueba 1 — Login exitoso

| Campo | Valor |
|---|---|
| Usuario | `juan.garcia` |
| Contraseña | `MiPassword123!` |
| Resultado esperado | Mensaje de acceso concedido |

## Captura 4 
![PreRequisitos](Capturas/SS03_AccesoOK.png)

**Resultado obtenido:** Muestra mensaje de éxito, validaciones ok.
**Captura de pantalla:** (adjuntar en el entregable)

---

#### Prueba 2 — Credenciales incorrectas

| Campo | Valor |
|---|---|
| Usuario | `juan.garcia` |
| Contraseña | `contraseñaIncorrecta` |
| Resultado esperado | Mensaje genérico de error + contador de intentos |

## Captura 5 
![PreRequisitos](Capturas/SS04_AccesoERROR.png)

**Resultado obtenido:** Se muestra un mensaje de error indicando que las credenciales son incorrectas y se informa la cantidad de intentos restantes antes del bloqueo de la cuenta.


**¿El mensaje revela si el usuario existe?** ☐ Sí ☑ No

**¿Por qué es importante que NO revele esta información?**

Porque si el sistema indica si un usuario existe o no, un atacante podría usar esa información para identificar cuentas válidas y realizar ataques dirigidos (como fuerza bruta o diccionario). Al mantener un mensaje genérico, se evita la enumeración de usuarios y se mejora la seguridad del sistema.

---

#### Prueba 3 — Intento de SQL Injection

Intenta los siguientes inputs en el campo **usuario**:

| Input | Resultado esperado | Resultado obtenido |
|---|---|---|
| `' OR '1'='1` | Acceso denegado | |
| `admin' --` | Acceso denegado | |
| `'; DROP TABLE usuarios; --` | Acceso denegado | |

**¿El sistema fue vulnerable?** ☐ Sí ☑ No

**¿Qué mecanismo del código previene el SQL Injection?**

El script seguro no cayó en la trampa porque utiliza **consultas preparadas** (el uso del signo `?` en el código de Python al consultar la base de datos). 

Al programarlo de esta manera, SQLite no ejecuta los textos extraños (como comillas o guiones) que metemos en las cajas de texto. El sistema los trata simplemente como si fueran el nombre de un usuario común y corriente. Como no existe ningún usuario llamado literalmente `' OR '1'='1`, el sistema lo rechaza de inmediato y protege la base de datos.

---

#### Prueba 4 — Bloqueo de cuenta

Intenta el login con usuario **maria.lopez** y una contraseña incorrecta 5 veces seguidas. En el intento 5, observa qué ocurre. Intenta con las credenciales correctas (`SecurePass456#`) después del bloqueo.

| Intento # | Contraseña usada | Resultado obtenido |
| :--- | :--- | :--- |
| 1 | mal1 | ERROR Acceso denegado. Credenciales incorrectas. Intentos restantes: 4 |
| 2 | mal2 | ERROR Acceso denegado. Credenciales incorrectas. Intentos restantes: 3 |
| 3 | mal3 | ERROR Acceso denegado. Credenciales incorrectas. Intentos restantes: 2 |
| 4 | mal4 | ERROR Acceso denegado. Credenciales incorrectas. Intentos restantes: 1 |
| 5 | mal5 | ERROR Acceso denegado. Cuenta bloqueada por intentos fallidos |
| 6 (con clave correcta) | SecurePass456# | OK Acceso correcto. Bienvenido (Rol) |

## Captura 6 
![PreRequisitos](Capturas/SS05_CuentaBlock.png)

**¿Cuál es el tiempo de bloqueo configurado en el sistema?** 15 minutos (`TIEMPO_BLOQUEO = 15`).

**Análisis del comportamiento observado:**
Al hacer la prueba, el sistema contó bien los 5 intentos y mostró el mensaje de cuenta bloqueada. Sin embargo, en el intento 6, al meter la clave correcta, el sistema me dejó entrar de todos modos sin esperar los 15 minutos. 

Esto pasa porque el código actual tiene un pequeño fallo de lógica: calcula y guarda la fecha de bloqueo en la base de datos, pero cuando llega una nueva petición, **no verifica si el usuario está bloqueado antes de validar la contraseña**. Si la clave es correcta, limpia los intentos y da acceso inmediato, ignorando el castigo del tiempo.



---

#### Prueba 5 — Intento de XSS en el campo usuario

| Input | Resultado esperado | Resultado obtenido |
| :--- | :--- | :--- |
| `<script>alert('XSS')</script>` o `<img src=x onerror=alert(1)>` | El script NO debe ejecutarse — debe aparecer como texto | ERROR Error. Datos demasiado largos. / Muestra el texto limpio en pantalla sin ejecutar nada. |

**Resultado obtenido:** Al meter el código largo con `<script>`, el sistema saltó de inmediato con el mensaje `"Datos demasiado largos"`, ya que al limpiar el texto los caracteres crecieron y superaron el límite de 50 permitido. Al probar con un ataque más corto, el sistema no ejecutó ninguna ventana de alerta y pintó los símbolos como texto común y corriente en la página de error.

**¿Qué función del código previene el XSS?**
Lo previenen dos cosas que pusimos en el código:
1. La función `html.escape()` de Python, que convierte los caracteres peligrosos como `<` y `>` en texto inofensivo (`&lt;` y `&gt;`), desarmando cualquier código que intente ejecutarse en el navegador.
2. El filtro de tamaño máximo (`MAX_USER_LEN`), que bloquea de golpe textos sospechosamente largos antes de que toquen la base de datos o la interfaz.

_________________________________________________________________________

---


### Prueba 6 — Revisar los logs de seguridad

Ver el log de autenticación generado (En Windows PowerShell)
Get-Content logs/auth.log

**¿Qué tipos de eventos aparecen en el log?**
Aparecen dos tipos de eventos bien diferenciados por su nivel de alerta:
1. `[INFO]`: Registra los accesos exitosos al sistema (`LOGIN_OK`).
2. `[WARNING]`: Registra los accesos denegados o fallidos (`LOGIN_FAIL`), lo que incluye tanto contraseñas incorrectas como los intentos de ataque.

**¿Qué información registra un evento de fallo?**
Cada línea de fallo guarda cuatro datos clave:
* La **fecha y hora exacta** del intento.
* El **nivel de peligro** (`[WARNING]`).
* El **usuario** que se intentó usar (si metieron código malicioso, queda guardado el texto limpio para ver qué querían hacer).
* La **dirección IP** desde donde se envió la petición (`127.0.0.1` en este caso local).

**¿Por qué es importante registrar los intentos fallidos?**
Es fundamental por dos razones prácticas:
1. **Auditoría y Alertas:** Si veo en el archivo que un usuario falla 5 veces seguidas en un minuto (como pasó con María), o si veo textos extraños con comillas y comandos SQL, sé de inmediato que alguien está intentando hackear la cuenta o probar vulnerabilidades.
2. **Fuerza Bruta:** Nos da la evidencia necesaria para saber si debemos bloquear una IP o banear a un usuario antes de que adivine la contraseña.

---

### Paso 5.4 — Verificar los Headers de Seguridad

Abre las herramientas de desarrollo del navegador (`F12` → pestaña `Network`) y examina los headers de respuesta:

**Headers presentes en la respuesta:**

| Header | ¿Presente? | Valor observado |
|---|---|---|
| `Strict-Transport-Security` | ☑ Sí ☐ No | `max-age=31536000; includeSubDomains` |
| `X-Content-Type-Options` | ☑ Sí ☐ No | `nosniff` |
| `X-Frame-Options` | ☑ Sí ☐ No | `DENY` |
| `Cache-Control` | ☑ Sí ☐ No | `no-store, no-cache, must-revalidate` |

**¿Para qué sirve el header `X-Frame-Options: DENY`?**
Sirve para prohibir por completo que nuestra página web sea incrustada o mostrada dentro de marcos (`<iframe>` o `<frame>`) de otros sitios web. 

Esto nos protege contra el ataque de **Clickjacking** (secuestro de clics), donde un atacante diseña una página falsa maliciosa y pone encima nuestro formulario de login de forma transparente para engañar al usuario, haciendo que rinda sus credenciales sin darse cuenta. Al recibir este header, el navegador bloquea la carga del cuadro y mantiene el sitio a salvo.

_________________________________________________________________________

---
## PARTE 6 — ANÁLISIS COMPARATIVO

### Paso 6.1 — Análisis del script inseguro vs seguro

Completa la tabla comparativa:

| Aspecto de seguridad | login_inseguro.py | login_seguro.py |
| :--- | :--- | :--- |
| **Protección SQL Injection** | **No tiene.** Junta el texto del usuario directo en la consulta, dejando que cualquiera entre usando comillas o guiones (`' OR '1'='1`). | **Sí tiene.** Usa el signo `?` para que el sistema trate lo que escriba el usuario como simple texto y no como código ejecutable. |
| **Almacenamiento de contraseñas** | **Inseguro.** Guarda y compara las claves en texto limpio, tal cual las escribe el usuario. | **Seguro.** Usa la librería `bcrypt` (factor 12) para convertir las claves en un código encriptado imposible de adivinar. |
| **Verificación de método HTTP** | **Ninguna.** Acepta cualquier forma de envío, lo que puede exponer los datos en la barra de direcciones. | **Estricta.** Solo permite peticiones por método `POST`. Si intentan entrar de otra forma, bloquea el acceso de inmediato. |
| **Protección XSS en output** | **No tiene.** Muestra los errores directo en la pantalla. Si metes código de programación, el navegador lo ejecuta. | **Sí tiene.** Usa `html.escape()` para desactivar etiquetas como `<script>` y pone un límite estricto de 50 caracteres al usuario. |
| **Manejo de intentos fallidos** | **Ninguno.** Permite fallar infinitas veces, ideal para que un atacante pruebe miles de claves hasta adivinar. | **Controlado.** Si fallas 5 veces seguidas, el sistema te bloquea el acceso por un tiempo establecido de 15 minutos. |
| **Logging de eventos** | **No tiene.** Si alguien entra a la fuerza o intenta hackear el sitio, no queda ningún rastro guardado. | **Sí tiene.** Guarda todo en el archivo `auth.log` registrando si el login fue correcto o falló, junto con la fecha, hora e IP. |
| **Mensajes de error** | **Inseguro.** Te avisa si el usuario no existe o si la clave está mal, dándole pistas al atacante para adivinar nombres reales. | **Seguro.** Muestra siempre un mensaje genérico ("Credenciales incorrectas") para no dar pistas de qué cuentas existen. |
| **Headers de seguridad HTTP** | **No envía ninguno.** Deja al navegador sin defensas contra trampas visuales o ataques web comunes. | **Completo.** Envía cabeceras fuertes como `X-Frame-Options: DENY` para evitar que clonen o metan nuestra página dentro de otra. |
| **Timing attack prevention** | **No tiene.** Responde más rápido si el usuario no existe, permitiendo adivinar nombres midiendo el tiempo de respuesta. | **Sí tiene.** Agrega un retraso artificial con `time.sleep(0.5)` y una validación falsa para que el servidor tarde siempre lo mismo. |
---

### Paso 6.2 — Análisis del hash bcrypt en la BD

Conéctate a la base de datos SQLite y examina los hashes:

```bash
# Abrir la BD con SQLite3
sqlite3 db/usuarios.db

# En la consola de SQLite:
SELECT usuario, substr(hash_password, 1, 29) as hash_parcial, rol 
FROM usuarios;

# ¿Cuál es el factor de coste visible en el hash?
-- El $12$ en $2b$12$... indica factor 12

# Verificar que dos usuarios con contraseñas diferentes tienen hashes diferentes:
SELECT LENGTH(hash_password) FROM usuarios LIMIT 1;

.quit
```


**¿Todos los hashes tienen el mismo prefijo `$2b$12$`?** ☑ Sí ☐ No

**¿Por qué todos los hashes tienen la MISMA longitud aunque las contraseñas sean distintas?**
Porque la librería `bcrypt` procesa la clave y, sin importar si es una palabra corta o una frase muy larga, el resultado comprimido (el hash) siempre tiene un tamaño fijo de **60 caracteres**. Esto se hace a propósito por seguridad, para que un atacante no pueda adivinar la longitud de la contraseña original mirando la base de datos.

**¿Podrías saber cuál usuario tiene la contraseña "más simple" solo mirando los hashes?** ☐ Sí ☑ No — **¿Por qué?**
No hay forma de saberlo. `bcrypt` genera una semilla aleatoria única (llamada "salt") para cada usuario antes de encriptar. Por eso, aunque dos usuarios tuvieran la misma contraseña simple, sus hashes se verán totalmente distintos y caóticos en la base de datos. Mirando la tabla, todos se ven igual de complejos.

---

## PARTE 7 — EJERCICIO DE EXTENSIÓN (AVANZADO)

### Desafío: Implementar CSRF Protection

El sistema actual tiene una vulnerabilidad pendiente: **CSRF (Cross-Site Request Forgery)**. Un atacante podría crear una página maliciosa que envíe un formulario POST a tu endpoint de login con las credenciales de otro usuario.

**Tu tarea:**

1. Investiga cómo funciona un token CSRF.
2. Modifica `login.html` para incluir un token CSRF oculto en el formulario.
3. Modifica `login_seguro.py` para validar ese token.

**Pista de implementación:**

```python
# En servidor o en generación de formulario:
import secrets
csrf_token = secrets.token_hex(32)   # Token criptográficamente seguro

# En el HTML del formulario:
# <input type="hidden" name="csrf_token" value="{{ csrf_token }}">

# En el CGI al recibir el POST:
# token_recibido = form.getvalue("csrf_token", "")
# if not hmac.compare_digest(token_recibido, token_esperado):
#     print(render_page("Error CSRF", "Token de seguridad inválido."))
#     exit(0)
```
## Captura 7 ![PreRequisitos](Capturas/SS06_TokenCSRF.png)

**Describe tu implementación:**

Modifiqué el login:
```python
<input type="hidden" name="csrf_token" value="4a8b92c4e1d3f5a7b93021f4e5d6c7b8a901ef23cd45bf6789abcdef01234567">
_________________________________________________________________________

Desde servidor_seguro.py:
```python
token_recibido = params.get("csrf_token", [""])[0]
TOKEN_ESPERADO = "4a8b92c4e1d3f5a7b93021f4e5d6c7b8a901ef23cd45bf6789abcdef01234567"
IP_CLIENTE = os.environ.get("REMOTE_ADDR", "?")

if not hmac.compare_digest(token_recibido, TOKEN_ESPERADO):
    logging.warning(f"POSIBLE_ATAQUE_CSRF ip={IP_CLIENTE}")
    print(render_page("Error de Seguridad", "Token CSRF inválido o ausente."))
    exit()
```
En la sección donde leo los datos CGI, agregué la captura del parámetro csrf_token y lo comparo directamente contra el valor que espera el sistema usando la función segura hmac.compare_digest(). Si el token no coincide o no viene, el script frena la ejecución, registra el intento sospechoso en el log con la IP del cliente y bloquea el acceso.

---

### Reflexión Final: Propuestas de Robustez

Para elevar el nivel de seguridad de nuestro `login_seguro.py` más allá del entorno actual de laboratorio, implementaría las siguientes 3 mejoras críticas:

1. **Implementar Sesiones y Tokens CSRF Dinámicos:** En lugar de usar un token estático fijo en el código, configuraría el backend para generar un token único y aleatorio por cada sesión activa utilizando `secrets.token_hex()`, almacenándolo temporalmente en una cookie segura con atributos `HttpOnly`, `Secure` y `SameSite=Strict`. Esto evitaría que el token pueda ser copiado o reutilizado permanentemente.

2. **Migración a un Framework Web Moderno (Descarte de CGI):**
   El estándar CGI es obsoleto, lento y propenso a fallos de configuración de variables de entorno en sistemas de producción. Cambiaría la infraestructura hacia un framework moderno como **FastAPI** o **Flask**. Esto permitiría un manejo nativo de peticiones, middleware automático para cabeceras de seguridad y una mejor gestión de dependencias y rutas.

3. **Bloqueo Avanzado por IP (Rate Limiting Real):**
   El bloqueo actual solo castiga al nombre de usuario en la base de datos, lo que permite que un atacante intente adivinar claves de muchos usuarios distintos a la vez (ataque de fuerza bruta distribuido). Implementaría un sistema de control de peticiones para rastrear la dirección `REMOTE_ADDR`, bloqueando por completo la IP de origen si supera un límite de solicitudes por minuto, protegiendo así todo el servidor.


## ENTREGABLE DEL LABORATORIO

Comprime la carpeta `lab_login_seguro/` y entrega los siguientes archivos. **IMPORTANTE: No incluir `server.key` en el entregable por seguridad.**

```
lab_login_seguro_APELLIDO_NOMBRE.zip
├── certs/
│   └── server.crt           ← Solo el certificado, NO la clave privada
├── cgi-bin/
│   ├── login_inseguro.py
│   └── login_seguro.py
├── www/
│   └── login.html
├── db/                      ← Solo si el docente lo solicita
├── logs/
│   └── auth.log             ← Log generado por tus pruebas
├── setup_db.py
├── servidor.py
└── INFORME_LAB2.md          ← Informe con tus respuestas y capturas
```


### Contenido del `INFORME_LAB2.md`

Tu informe debe incluir:

1. **Resumen ejecutivo** (5-7 líneas): ¿Qué hiciste, qué aprendiste?
2. **Captura del certificado SSL** (del navegador mostrando la advertencia y la info del certificado)
3. **Captura de login exitoso**
4. **Captura del log de autenticación** (`auth.log`)
5. **Respuestas a todas las preguntas de reflexión** de las partes 1-6
6. **Tabla comparativa** completada (Paso 6.1)
7. **Vulnerabilidades identificadas** en el script inseguro
8. **Reflexión final**: ¿Qué cambiarías en el login seguro para hacerlo más robusto? Menciona al menos 3 mejoras posibles.

---

## CRITERIOS DE EVALUACIÓN

| Criterio | Peso | Descripción |
|---|---|---|
| **Certificado SSL generado y funcional** | 15% | OpenSSL correcto, certificado válido, servidor HTTPS activo |
| **Script CGI seguro funcional** | 30% | Login funciona, verifica bcrypt, maneja errores correctamente |
| **Pruebas documentadas** | 25% | Todas las pruebas completadas con resultados y capturas |
| **Análisis de vulnerabilidades** | 15% | Identificación correcta de errores en script inseguro |
| **Informe y reflexión** | 15% | Respuestas reflexivas y completas, redacción clara |

---

## REFERENCIAS DEL LABORATORIO

- **Documentación bcrypt Python**: https://pypi.org/project/bcrypt/
- **Python http.server CGI**: https://docs.python.org/3/library/http.server.html
- **Python ssl module**: https://docs.python.org/3/library/ssl.html
- **OpenSSL Commands Reference**: https://www.openssl.org/docs/man1.1.1/man1/
- **OWASP Authentication Cheat Sheet**: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- **OWASP CSRF Prevention**: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
- **SQLite3 Python**: https://docs.python.org/3/library/sqlite3.html

---

*Guía de Laboratorio — Semana 2 | Programación Segura DD281 | Universidad Autónoma del Perú | 2026-1*