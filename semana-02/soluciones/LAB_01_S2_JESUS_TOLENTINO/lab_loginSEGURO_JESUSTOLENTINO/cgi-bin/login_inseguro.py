#!/usr/bin/env python3
"""Ejemplo intencionalmente vulnerable. No usar en producción."""
import os
import sqlite3
from urllib.parse import parse_qs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "usuarios.db")

body = os.environ.get("CGI_BODY", "")
form = parse_qs(body)
usuario = form.get("usuario", [""])[0]
password = form.get("password", [""])[0]

print("Content-Type: text/html; charset=utf-8\n")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
# VULNERABLE: concatenación directa y comparación incorrecta.
sql = (
    f"SELECT * FROM usuarios WHERE usuario='{usuario}' "
    f"AND hash_password='{password}'"
)
cursor.execute(sql)
fila = cursor.fetchone()

if fila:
    print(f"<h1>Bienvenido {usuario}</h1>")
    print(f"<p>Registro completo: {fila}</p><p>Contraseña: {password}</p>")
else:
    existe = cursor.execute(
        f"SELECT id FROM usuarios WHERE usuario='{usuario}'"
    ).fetchone()
    if existe:
        print("<h1>Contraseña incorrecta para ese usuario</h1>")
    else:
        print(f"<h1>El usuario '{usuario}' no existe</h1>")
conn.close()
