from flask import Flask, session, redirect, url_for, request, abort
from datetime import timedelta
import secrets
from functools import wraps   # ✅ Importante

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.permanent_session_lifetime = timedelta(minutes=15)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="Strict"
)

# 🎭 Decorador RBAC corregido
def require_role(roles):
    def decorator(f):
        @wraps(f)   # ✅ Esto preserva el nombre original de la función
        def wrapper(*args, **kwargs):
            if "role" not in session:
                return redirect(url_for("login"))
            if session["role"] not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario")
    rol = request.form.get("rol")
    session.permanent = True
    session["user_id"] = usuario
    session["role"] = rol
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@require_role(["cliente", "operador", "admin"])
def dashboard():
    return f"Bienvenido {session['role']} {session['user_id']}"

@app.route("/admin")
@require_role(["admin"])
def admin_panel():
    return "Panel de administración seguro"

@app.route("/operaciones")
@require_role(["operador", "admin"])
def operaciones():
    return "Gestión de operaciones bancarias"

@app.route("/cuenta")
@require_role(["cliente"])
def cuenta():
    return "Acceso a cuenta personal del cliente"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # sin ssl_context
