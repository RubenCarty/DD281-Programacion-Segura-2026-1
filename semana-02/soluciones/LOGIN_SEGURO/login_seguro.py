#!/usr/bin/env python3
# Script seguro con bcrypt y prepared statements
import cgi
import sqlite3
import bcrypt
import html
import os

print("Content-Type: text/html")
print()

def render(titulo, mensaje, exito=False):
    color = "#48bb78" if exito else "#e94560"
    return f"<h1 style='color:{color}'>{titulo}</h1><p>{mensaje}</p><a href='/login.html'>Volver</a>"

form = cgi.FieldStorage()
usuario = form.getvalue("usuario", "")
password = form.getvalue("password", "")

conn = sqlite3.connect("../db/usuarios.db")
cursor = conn.cursor()
cursor.execute("SELECT hash_password, rol FROM usuarios WHERE usuario = ?", (usuario,))
fila = cursor.fetchone()
conn.close()

if fila and bcrypt.checkpw(password.encode(), fila[0].encode()):
    print(render("✅ Acceso concedido", f"Bienvenido {html.escape(usuario)}", True))
else:
    print(render("❌ Acceso denegado", "Credenciales incorrectas"))
