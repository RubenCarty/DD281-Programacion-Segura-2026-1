#!/usr/bin/env python3
# Script con VULNERABILIDADES - NO USAR EN PRODUCCIÓN
import cgi
import sqlite3

print("Content-Type: text/html")
print()

form = cgi.FieldStorage()
usuario = form.getvalue("usuario", "")

conn = sqlite3.connect("../db/usuarios.db")
cursor = conn.cursor()
# VULNERABLE A SQL INJECTION
cursor.execute(f"SELECT * FROM usuarios WHERE usuario = '{usuario}'")
fila = cursor.fetchone()
conn.close()

if fila:
    print(f"<h1>Bienvenido {usuario}</h1>")
else:
    print(f"<h1>Usuario {usuario} no existe</h1>")
print('<a href="/login.html">Volver</a>')
