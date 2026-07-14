from flask import Flask, request, session, jsonify, redirect
import sqlite3, os

app = Flask(__name__)
app.secret_key = "clave123"  # ❌ Clave débil y hardcodeada
app.config['SESSION_COOKIE_HTTPONLY'] = False  # ❌
app.config['SESSION_COOKIE_SECURE'] = False    # ❌

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
    username = request.form.get('username')
    password = request.form.get('password')
    conn = get_db()
    user = conn.execute(f"SELECT * FROM usuarios WHERE username='{username}' AND password='{password}'").fetchone()
    conn.close()
    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({"mensaje": f"Bienvenido {user['username']}", "user_id": user['id']})
    return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route('/comentario/nuevo', methods=['POST'])
def nuevo_comentario():
    if not session.get('user_id'):
        return jsonify({"error": "No autenticado"}), 401
    contenido = request.form.get('contenido', '')
    conn = get_db()
    conn.execute(f"INSERT INTO comentarios (contenido, autor_id) VALUES ('{contenido}', {session['user_id']})")
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Comentario guardado"})

@app.route('/comentarios')
def ver_comentarios():
    conn = get_db()
    comentarios = conn.execute("SELECT contenido FROM comentarios").fetchall()
    conn.close()
    html = "<html><body><h1>Comentarios</h1>"
    for c in comentarios:
        html += f"<div>{c['contenido']}</div>"  # ❌ Sin escape
    html += "</body></html>"
    return html

@app.route('/documento/<int:doc_id>')
def ver_documento(doc_id):
    if not session.get('user_id'):
        return redirect('/login')
    conn = get_db()
    doc = conn.execute("SELECT * FROM documentos WHERE id = ?", (doc_id,)).fetchone()
    conn.close()
    if doc:
        return jsonify({"titulo": doc['titulo'], "contenido": doc['contenido']})
    return jsonify({"error": "No encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)
