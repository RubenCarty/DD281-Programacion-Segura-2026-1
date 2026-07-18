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