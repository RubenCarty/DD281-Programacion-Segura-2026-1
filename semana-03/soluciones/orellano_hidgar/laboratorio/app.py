from datetime import datetime, timedelta
from functools import wraps
import hashlib
import secrets
import time

from flask import Flask, abort, make_response, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.config.update(
    SECRET_KEY=secrets.token_hex(32),
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,  # En produccion debe ser True con HTTPS.
    SESSION_COOKIE_SAMESITE="Lax",
)

USUARIOS = {
    "admin@test.com": {"password": "Admin2026!", "role": "admin", "nombre": "Ana Admin"},
    "supervisor@test.com": {"password": "Super2026!", "role": "supervisor", "nombre": "Pedro Supervisor"},
    "usuario@test.com": {"password": "Usuario2026!", "role": "usuario", "nombre": "Hidgar Usuario"},
}

sesiones_auditoria = {}


def hash_session_id(raw_session_id: str) -> str:
    if not raw_session_id:
        return "sin-cookie"
    return hashlib.sha256(raw_session_id.encode("utf-8")).hexdigest()[:16]


def registrar_auditoria():
    sid = hash_session_id(request.cookies.get(app.config["SESSION_COOKIE_NAME"], ""))
    sesiones_auditoria[sid] = {
        "usuario": session.get("user_id"),
        "ip": request.remote_addr or "local",
        "login_at": sesiones_auditoria.get(sid, {}).get("login_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))
            session.permanent = True
            registrar_auditoria()
            if session.get("user_role") not in roles:
                return render_template("error.html", code=403, msg=f"Acceso denegado. Requiere: {roles}"), 403
            return f(*args, **kwargs)
        return inner
    return decorator


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = USUARIOS.get(email)

        if user and secrets.compare_digest(user["password"], password):
            session.clear()  # Previene Session Fixation antes de asignar identidad.
            session["user_id"] = email
            session["user_role"] = user["role"]
            session["user_name"] = user["nombre"]
            session["login_time"] = int(time.time())
            session.permanent = True
            response = redirect(url_for("dashboard"))
            return response

        return render_template("login.html", error="Credenciales incorrectas"), 401

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", name=session["user_name"], role=session["user_role"])


@app.route("/logout")
def logout():
    session.clear()
    response = make_response(redirect(url_for("login")))
    response.delete_cookie(app.config["SESSION_COOKIE_NAME"])
    return response


@app.route("/mi-perfil")
@require_role("admin", "supervisor", "usuario")
def mi_perfil():
    return render_template("dashboard.html", name=session["user_name"], role=session["user_role"], seccion="Mi Perfil")


@app.route("/reportes")
@require_role("admin", "supervisor")
def ver_reportes():
    reportes = [
        {"titulo": "Reporte de Accesos", "fecha": "2026-06-15"},
        {"titulo": "Reporte de Sesiones", "fecha": "2026-06-14"},
        {"titulo": "Reporte de Incidentes", "fecha": "2026-06-13"},
    ]
    return render_template("dashboard.html", name=session["user_name"], role=session["user_role"], seccion="Reportes", reportes=reportes)


@app.route("/admin/panel")
@require_role("admin")
def panel_admin():
    return render_template("admin.html", usuarios=USUARIOS, sesiones=sesiones_auditoria)


@app.route("/admin/usuarios/<path:email>/eliminar", methods=["POST"])
@require_role("admin")
def eliminar_usuario(email):
    email = email.strip().lower()
    if email == session.get("user_id"):
        return render_template("error.html", code=400, msg="El administrador no puede eliminarse a si mismo."), 400
    if email not in USUARIOS:
        abort(404)
    usuario = USUARIOS[email]
    return render_template("error.html", code=200, msg=f"Simulacion: usuario {email} con rol {usuario['role']} eliminado correctamente."), 200


@app.route("/admin/sesiones-activas")
@require_role("admin")
def sesiones_activas():
    return render_template("admin.html", usuarios=USUARIOS, sesiones=sesiones_auditoria, solo_sesiones=True)


@app.route("/demo/fixation")
def demo_fixation():
    session_id_antes = request.cookies.get(app.config["SESSION_COOKIE_NAME"], "Sin sesion previa")
    info = {
        "session_id_antes_login": session_id_antes[:20] + "..." if len(session_id_antes) > 20 else session_id_antes,
        "tiene_user_id": "user_id" in session,
        "nota": "Despues del login, la sesion se limpia con session.clear() antes de asignar identidad.",
    }
    return info


@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5000)
