from flask import Flask, request, session, jsonify, redirect, make_response
import sqlite3, html, secrets, re
from functools import wraps

app = Flask(__name__)

# TODO 1 COMPLETADO: Usar secrets.token_hex(32) para la clave secreta
# Previene: Predictable Cryptographic Keys (OWASP A02:2021 - Cryptographic Failures)
# Cómo funciona: secrets.token_hex(32) genera 64 caracteres hexadecimales (256 bits)
# de entropía criptográficamente aleatoria, imposible de adivinar por fuerza bruta.
app.secret_key = secrets.token_hex(32)

# TODO 2 COMPLETADO: Configurar las 3 propiedades de seguridad de la cookie de sesión
# Previene: Session Hijacking via XSS (OWASP A07:2021 - Identification and Authentication Failures)
# HttpOnly=True impide que JavaScript lea la cookie (bloquea robo via XSS).
# Secure=True asegura que la cookie solo viaje por HTTPS (evita sniffing en HTTP).
# SameSite=Strict previene ataques CSRF al bloquear envío de cookie cross-site.
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

def requiere_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({"error": "No autenticado"}), 401
        return f(*args, **kwargs)
    return decorated

def get_db():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE usuarios (id INTEGER PRIMARY KEY, username TEXT, password TEXT);
        CREATE TABLE comentarios (id INTEGER PRIMARY KEY, contenido TEXT, autor_id INTEGER);
        CREATE TABLE documentos (id INTEGER PRIMARY KEY, titulo TEXT, contenido TEXT, propietario_id INTEGER);
        INSERT INTO usuarios VALUES (1, 'admin', 'Admin123!');
        INSERT INTO usuarios VALUES (2, 'carlos', 'Carlos456!');
        INSERT INTO comentarios VALUES (1, 'Bienvenidos al foro seguro', 1);
        INSERT INTO documentos VALUES (1, 'Contrato Confidencial', 'Datos sensibles del contrato...', 1);
        INSERT INTO documentos VALUES (2, 'Mi documento personal', 'Datos de Carlos...', 2);
    ''')
    conn.commit()
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    # TODO 3 COMPLETADO: Validar que username solo contenga letras, números y guiones (regex)
    # Previene: Input Injection / SQL Injection (OWASP A03:2021 - Injection)
    # Cómo funciona: El regex limita los caracteres aceptados en el username, rechazando
    # caracteres especiales usados en inyección SQL antes de que lleguen a la consulta.
    if not re.match(r'^[a-zA-Z0-9_-]{3,30}$', username):
        return jsonify({"error": "Username inválido"}), 400

    conn = get_db()

    # TODO 4 COMPLETADO: Usar consulta parametrizada (prepared statement) para prevenir SQL Injection
    # Previene: SQL Injection (OWASP A03:2021 - Injection)
    # Cómo funciona: Los parámetros (?) son enviados separados del SQL; el motor de base
    # de datos los trata siempre como datos, nunca como código ejecutable.
    user = conn.execute(
        "SELECT * FROM usuarios WHERE username=? AND password=?",
        (username, password)
    ).fetchone()
    conn.close()

    if user:
        # TODO 5 COMPLETADO: Regenerar el session ID después del login (previene Session Fixation)
        # Previene: Session Fixation (OWASP A07:2021 - Identification and Authentication Failures)
        # Cómo funciona: session.clear() descarta el ID de sesión previo (que podría haber
        # sido fijado por un atacante) y Flask genera un nuevo ID limpio tras asignar los datos.
        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        # Nota de seguridad: NO se devuelve user_id en la respuesta (evita enumeración de IDs)
        return jsonify({"mensaje": f"Bienvenido {user['username']}"})
    return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route('/comentario/nuevo', methods=['POST'])
@requiere_login
def nuevo_comentario():
    contenido = request.form.get('contenido', '').strip()

    # TODO 6 COMPLETADO: Validar longitud máxima del comentario (máximo 500 caracteres)
    # Previene: DoS por datos masivos / Stored XSS payload oversized (OWASP A03, A05)
    # Cómo funciona: Rechazar entradas que excedan el límite protege la BD y reduce
    # la superficie de ataque para inyección de payloads muy largos.
    if len(contenido) > 500:
        return jsonify({"error": "El comentario no puede superar los 500 caracteres"}), 400

    conn = get_db()
    # TODO 7 COMPLETADO: Usar consulta parametrizada para insertar el comentario
    # Previene: SQL Injection (OWASP A03:2021 - Injection)
    # Cómo funciona: Los valores se pasan como parámetros separados del texto SQL,
    # por lo que caracteres como comillas simples son datos, no delimitadores de consulta.
    conn.execute(
        "INSERT INTO comentarios (contenido, autor_id) VALUES (?, ?)",
        (contenido, session['user_id'])
    )
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Comentario guardado"})

@app.route('/comentarios')
def ver_comentarios():
    conn = get_db()
    comentarios = conn.execute("SELECT contenido FROM comentarios").fetchall()
    conn.close()

    html_content = "<html><body><h1>Comentarios</h1>"
    for c in comentarios:
        # TODO 8 COMPLETADO: Escapar el contenido con html.escape() antes de incluirlo en HTML
        # Previene: Cross-Site Scripting (XSS) Almacenado (OWASP A03:2021 - Injection)
        # Cómo funciona: html.escape() convierte caracteres especiales HTML (<, >, ", ', &)
        # en entidades HTML (&lt; &gt; etc.), por lo que el navegador los muestra como
        # texto plano en vez de interpretarlos como etiquetas ejecutables.
        contenido_seguro = html.escape(c['contenido'])
        html_content += f"<div>{contenido_seguro}</div>"
    html_content += "</body></html>"
    return html_content

@app.route('/documento/<int:doc_id>')
@requiere_login
def ver_documento(doc_id):
    usuario_id = session['user_id']
    conn = get_db()

    # TODO 9 COMPLETADO: Verificar que el documento pertenece al usuario en sesión
    # Previene: Insecure Direct Object Reference - IDOR (OWASP A01:2021 - Broken Access Control)
    # Cómo funciona: Agregar la condición propietario_id=? hace que la consulta devuelva
    # NULL si el documento existe pero pertenece a otro usuario, bloqueando el acceso cruzado.
    doc = conn.execute(
        "SELECT * FROM documentos WHERE id=? AND propietario_id=?",
        (doc_id, usuario_id)
    ).fetchone()
    conn.close()

    if doc:
        return jsonify({"titulo": doc['titulo'], "contenido": doc['contenido']})

    # TODO 10 COMPLETADO: Devolver MISMO error 404 tanto si no existe como si no pertenece al usuario
    # Previene: Information Disclosure / IDOR enumeration (OWASP A01:2021 - Broken Access Control)
    # Cómo funciona: Usar el mismo mensaje y código HTTP 404 en ambos casos (no existe /
    # no autorizado) impide que un atacante distinga entre IDs válidos e inválidos,
    # dificultando la enumeración de recursos ajenos.
    return jsonify({"error": "Documento no encontrado"}), 404

@app.after_request
def agregar_headers_seguridad(response):
    # TODO 11 COMPLETADO: Agregar Content-Security-Policy header
    # Previene: Cross-Site Scripting (XSS) y Data Injection (OWASP A03:2021 - Injection)
    # Cómo funciona: El header CSP le indica al navegador que solo ejecute scripts y
    # cargue recursos del mismo origen ('self'), bloqueando scripts inline y de dominios
    # externos aunque un atacante logre inyectar HTML malicioso en la página.
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response

if __name__ == '__main__':
    app.run(debug=False, port=5002)  # ✅ debug=False en producción
