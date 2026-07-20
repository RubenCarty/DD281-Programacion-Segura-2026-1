from flask import Flask, session, redirect, url_for, request, make_response, render_template
import secrets

# 1. Crear la aplicación Flask
app = Flask(__name__)

# 2. Configuración de seguridad de sesiones
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config.update(
    SESSION_COOKIE_HTTPONLY = True,     # Evita acceso vía JavaScript
    SESSION_COOKIE_SECURE   = False,    # True en producción con HTTPS
    SESSION_COOKIE_SAMESITE = 'Strict', # Protege contra CSRF
)

# ─── USUARIOS DE PRUEBA ───────────────────────────────
USUARIOS = {
    'admin@test.com':      {'password': 'Admin2026!',   'role': 'admin',      'nombre': 'Ana Admin'},
    'supervisor@test.com': {'password': 'Super2026!',   'role': 'supervisor', 'nombre': 'Pedro Sup'},
    'usuario@test.com':    {'password': 'Usuario2026!', 'role': 'usuario',    'nombre': 'María User'},
}

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        user = USUARIOS.get(email)
        if user and user['password'] == password:
            # Prevención de Session Fixation
            session.clear()
            session['user_id']    = email
            session['user_role']  = user['role']
            session['user_name']  = user['nombre']
            session.permanent     = True
            return redirect(url_for('dashboard'))

        return render_template('login.html', error='Credenciales incorrectas')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html',
                           name=session['user_name'],
                           role=session['user_role'])

@app.route('/logout')
def logout():
    # Logout correcto: servidor + cliente
    session.clear()
    resp = redirect(url_for('login'))
    resp.delete_cookie('session')
    return resp

if __name__ == '__main__':
    app.run(debug=True, port=5000)
